"""Zgłasza adresy z sitemapy do IndexNow (Bing i inne wyszukiwarki) po udanym wdrożeniu."""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "web" / "dist"
HOST = "drmartakryczka.pl"
KEY_FILES = sorted((ROOT / "web" / "public").glob("*.txt"))


def indexnow_key():
    for path in KEY_FILES:
        text = path.read_text(encoding="utf-8").strip()
        if path.stem == text and re.fullmatch(r"[0-9a-f]{32}", text):
            return text
    sys.exit("Brak pliku z kluczem IndexNow (web/public/<klucz>.txt, treść = nazwa pliku)")


def sitemap_urls():
    urls = []
    for sitemap in sorted(DIST.glob("sitemap-*.xml")):
        if sitemap.name == "sitemap-index.xml":
            continue
        urls += re.findall(r"<loc>(https://%s/[^<]*)</loc>" % re.escape(HOST), sitemap.read_text(encoding="utf-8"))
    return urls


def main():
    key = indexnow_key()
    urls = sitemap_urls()
    if not urls:
        sys.exit("Sitemapa nie zawiera adresów")
    body = json.dumps({
        "host": HOST,
        "key": key,
        "keyLocation": "https://{}/{}.txt".format(HOST, key),
        "urlList": urls,
    }).encode()
    request = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=body,
        headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(request, timeout=30) as response:
        print("IndexNow status", response.status, "dla", len(urls), "adresów")


if __name__ == "__main__":
    main()
