"""Sprawdza zbudowaną stronę (web/dist) pod kątem reguł z docs/seo-najlepsze-praktyki.md.

Błędy (kod wyjścia 1) blokują wdrożenie, ostrzeżenia tylko informują.
Uruchomienie: cd web && npm run build && cd .. && python3 .github/scripts/seo_check.py
"""
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "web" / "dist"
SITE = "https://drmartakryczka.pl"
TITLE_MAX = 70
TITLE_WARN = 60
DESC_MAX = 165
DESC_MIN = 70
# Klasy obrazów o stałych proporcjach w CSS (nie powodują CLS bez width/height).
CSS_SIZED_CLASSES = {"card-img", "banner", "device-img"}
CI = os.environ.get("GITHUB_ACTIONS") == "true"

errors, warnings = [], []


def report(level, page, message):
    (errors if level == "error" else warnings).append((page, message))
    if CI:
        print("::%s::%s: %s" % (level, page, message))
    else:
        print("%s %s: %s" % ("BŁĄD " if level == "error" else "uwaga", page, message))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.in_title = False
        self.meta = {}
        self.canonical = None
        self.alternates = []
        self.robots = ""
        self.headings = []
        self.imgs = []
        self.links = []
        self.jsonld = []
        self._script = None
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
            if (a.get("name") or "").lower() == "robots":
                self.robots = (a.get("content") or "").lower()
        elif tag == "link":
            rel = a.get("rel", "")
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and a.get("hreflang"):
                self.alternates.append((a["hreflang"], a.get("href", "")))
        elif re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._script = True
            self._buf = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self._script:
            self.jsonld.append(self._buf)
            self._script = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self._script:
            self._buf += data


def url_path(file):
    rel = file.relative_to(DIST).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def resolves(path):
    path = unquote(path.split("#")[0].split("?")[0])
    if not path.startswith("/"):
        return True
    target = DIST / path.lstrip("/")
    if path.endswith("/"):
        return (target / "index.html").exists()
    return target.is_file() or (target / "index.html").exists()


def types_in(node):
    found = []
    if isinstance(node, list):
        for item in node:
            found += types_in(item)
    elif isinstance(node, dict):
        t = node.get("@type")
        found += t if isinstance(t, list) else [t]
        for value in node.values():
            found += types_in(value)
    return found


def main():
    if not DIST.exists():
        sys.exit("Brak web/dist. Najpierw uruchom: cd web && npm run build")

    pages = {}
    for file in sorted(DIST.rglob("*.html")):
        if file.name not in ("index.html", "404.html"):
            continue  # np. plik weryfikacyjny Google Search Console
        parser = Page()
        parser.feed(file.read_text(encoding="utf-8"))
        pages[url_path(file)] = parser

    indexable = {p: d for p, d in pages.items() if "noindex" not in d.robots and p != "/404.html"}
    titles, descriptions = {}, {}
    article_pages = set()

    for path, page in sorted(indexable.items()):
        title = page.title.strip()
        description = page.meta.get("description", "").strip()

        if not title:
            report("error", path, "brak <title>")
        else:
            if len(title) > TITLE_MAX:
                report("error", path, "title ma %d znaków (maks. %d)" % (len(title), TITLE_MAX))
            elif len(title) > TITLE_WARN:
                report("warning", path, "title ma %d znaków (zalecane do %d)" % (len(title), TITLE_WARN))
            titles.setdefault(title, []).append(path)

        if not description:
            report("error", path, "brak meta description")
        else:
            if len(description) > DESC_MAX:
                report("error", path, "description ma %d znaków (maks. %d)" % (len(description), DESC_MAX))
            elif len(description) < DESC_MIN:
                report("warning", path, "description ma %d znaków (zalecane od %d)" % (len(description), DESC_MIN))
            descriptions.setdefault(description, []).append(path)

        expected = SITE + path
        if page.canonical != expected:
            report("error", path, "canonical to %r, oczekiwano %r" % (page.canonical, expected))

        h1 = page.headings.count(1)
        if h1 != 1:
            report("error", path, "powinien być dokładnie jeden H1, jest %d" % h1)
        previous = 0
        for level in page.headings:
            if previous and level > previous + 1:
                report("warning", path, "nagłówek h%d po h%d (pominięty poziom)" % (level, previous))
                break
            previous = level

        for key in ("og:title", "og:description", "og:url", "og:image", "og:type", "og:site_name", "og:locale", "twitter:card"):
            if not page.meta.get(key):
                report("error", path, "brak znacznika %s" % key)
        if page.meta.get("og:image") and not page.meta["og:image"].startswith("https://"):
            report("error", path, "og:image musi być absolutnym adresem https")

        for hreflang, href in page.alternates:
            target = urlparse(href).path
            if not href.startswith(SITE) or target not in pages:
                report("error", path, "hreflang=%s wskazuje nieistniejącą stronę %s" % (hreflang, href))

        if not page.jsonld:
            report("error", path, "brak danych strukturalnych JSON-LD")
        for raw in page.jsonld:
            try:
                data = json.loads(raw)
            except ValueError as exc:
                report("error", path, "niepoprawny JSON-LD: %s" % exc)
                continue
            bad = {"Review", "AggregateRating"} & set(types_in(data))
            if bad:
                report("error", path, "%s bez prawdziwych opinii jest niedozwolone" % ", ".join(sorted(bad)))
            if "Article" in types_in(data):
                article_pages.add(path)

    for title, where in titles.items():
        if len(where) > 1:
            report("error", ", ".join(where), "powtórzony title: %r" % title)
    for description, where in descriptions.items():
        if len(where) > 1:
            report("error", ", ".join(where), "powtórzony description")

    seen_images = set()
    for path, page in sorted(pages.items()):
        for img in page.imgs:
            src = img.get("src", "")
            if "alt" not in img:
                report("error", path, "obraz bez atrybutu alt: %s" % src)
            if src.startswith("/") and not resolves(src):
                report("error", path, "brak pliku obrazu %s" % src)
            if src in seen_images:
                continue
            seen_images.add(src)
            # Puste alt jest w porządku dla ozdobnych obrazów kart, ale nie w treści wpisu.
            if "alt" in img and not img["alt"].strip() and path in article_pages:
                report("warning", path, "obraz z pustym alt w treści wpisu: %s" % src)
            if src.startswith("/") and not (img.get("width") and img.get("height")):
                css_sized = set(img.get("class", "").split()) & CSS_SIZED_CLASSES or src.startswith("/img/logos/")
                if not css_sized:
                    report("warning", path, "obraz bez width/height (ryzyko CLS): %s" % src)
        for href in page.links:
            if href.startswith(SITE):
                href = href[len(SITE):] or "/"
            if href.startswith("/") and not href.startswith("//") and not resolves(href):
                report("error", path, "martwy link wewnętrzny: %s" % href)

    sitemap_urls = []
    for sitemap in sorted(DIST.glob("sitemap-*.xml")):
        if sitemap.name == "sitemap-index.xml":
            continue
        text = sitemap.read_text(encoding="utf-8")
        sitemap_urls += re.findall(r"<loc>([^<]+)</loc>", text)
        if text.count("<loc>") != text.count("<lastmod>"):
            report("error", sitemap.name, "każdy adres w sitemapie powinien mieć <lastmod>")
    in_sitemap = {urlparse(u).path for u in sitemap_urls}
    for path in sorted(indexable):
        if path not in in_sitemap:
            report("error", path, "indeksowalna strona nie jest w sitemapie")
    for path in sorted(in_sitemap):
        if path not in indexable:
            report("error", path, "w sitemapie jest strona noindex lub nieistniejąca")

    robots = DIST / "robots.txt"
    if not robots.exists() or "Sitemap: %s/sitemap-index.xml" % SITE not in robots.read_text(encoding="utf-8"):
        report("error", "robots.txt", "brak linii Sitemap z pełnym adresem sitemap-index.xml")
    if not any(re.fullmatch(r"[0-9a-f]{32}\.txt", f.name) for f in DIST.glob("*.txt")):
        report("error", "IndexNow", "brak pliku klucza <32 znaki hex>.txt w katalogu głównym")

    print("\nSprawdzono %d stron (%d indeksowalnych): %d błędów, %d ostrzeżeń." % (len(pages), len(indexable), len(errors), len(warnings)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
