# SEO – najlepsze praktyki dla strony drmartakryczka.pl

Dokument obowiązuje przy **każdym** dodaniu lub zmianie strony, artykułu, aktualności, obrazu, linku
albo szablonu. Reguły techniczne pilnuje skrypt `.github/scripts/seo_check.py` (patrz „Automatyczna kontrola”);
pozostałe punkty to lista kontrolna dla osoby (lub agenta) wprowadzającej zmianę.

## Automatyczna kontrola

```bash
cd web && npm run build && cd .. && python3 .github/scripts/seo_check.py
```

- **Błędy blokują wdrożenie** (`deploy.yml`) i pull request (`seo-check.yml`). Ostrzeżenia tylko informują, ale
  traktuj je jako zadanie do wykonania.
- Skrypt sprawdza zbudowane `web/dist`: title, description, canonical, jeden H1, kolejność nagłówków, Open Graph
  i Twitter, hreflang, JSON-LD (zakaz `Review`/`AggregateRating`), duplikaty title/description, `alt` i pliki obrazów,
  martwe linki wewnętrzne, sitemapę (`lastmod`, brak stron `noindex`), `robots.txt` i plik klucza IndexNow.
- Nie zastępuje myślenia: nie oceni, czy treść jest rzetelna, unikalna i pomocna.

## 1. Treść i intencja

- Jedna strona = jeden temat i konkretna intencja czytelnika (pytanie pacjenta, informacja dla lekarza). Bez „cienkich”
  stron: nowa strona musi wnosić wartość, której nie ma gdzie indziej na stronie.
- Treść medyczna: rzetelnie, neutralnie, z ograniczeniami i wskazaniami; **bez obietnic rezultatów**, bez
  porównań „najlepszy”, bez zmyślonych opinii, danych, adresów, godzin i kwalifikacji. Dane, których nie mamy,
  oznaczamy „Do uzupełnienia” i prosimy o nie Martę.
- Autor i data: artykuły mają `date`, a po istotnej zmianie treści ustaw `updated` (trafia do `dateModified`
  i `lastmod` w sitemapie).
- Pisz do ludzi: krótkie akapity, nagłówki opisujące treść, fraza kluczowa naturalnie w tytule, pierwszym akapicie
  i nagłówkach, bez upychania słów kluczowych.
- Linkowanie wewnętrzne: każdy nowy wpis linkuje do 2–3 powiązanych podstron (Zabiegi, Szkolenia, inny artykuł)
  z opisowym tekstem linku (nie „kliknij tutaj”) i jest linkowany z co najmniej jednej istniejącej strony
  (lista artykułów/aktualności robi to automatycznie).

## 2. Title i description

- `title`: razem z sufiksem „ | dr Marta Kryczka” maks. **60 znaków** (twardy limit skryptu: 70). Dlatego
  `seoTitle` we frontmatterze ma maks. **41 znaków**. Zaczynaj od frazy, nie od nazwy gabinetu.
- `description` / `seoDescription`: **70–160 znaków**, konkretna zachęta do kliknięcia, bez cudzysłowów i bez
  obietnic. Unikalna na każdej stronie (duplikaty to błąd).
- Title i description muszą się różnić od wszystkich innych stron i wersji językowej.

## 3. Nagłówki

- Dokładnie **jeden `<h1>`** na stronie (w szablonie lub treści), potem `h2` → `h3` bez przeskoków.
- W treści Markdown zaczynaj od `##`, bo `h1` jest tytułem wpisu z szablonu.
- Listy kart (aktualności, artykuły, zabiegi) mają nagłówki kart jako `h2`.

## 4. Obrazy (Core Web Vitals)

- Format **WebP**, własne zdjęcia lub okładki z tego konkretnego materiału (patrz `AGENTS.md`), zapisane w
  `web/public/img/`. Nazwa pliku opisowa, małymi literami, myślnikami (np. `kongres-ptmeiaa-prezentacja-blizny-laser-2026.webp`).
- Każdy obraz ma **`alt`** w PL i EN opisujący, co widać (nie „zdjęcie”, nie lista słów kluczowych). Puste `alt=""`
  tylko dla czysto ozdobnych obrazów.
- Obrazy w treści `.md` pisane składnią Markdown dostają `loading="lazy"`, `decoding="async"` i `width`/`height`
  automatycznie. **Surowe `<img>` w Markdownie plugin pomija**: wpisz `width`/`height` (rzeczywiste wymiary pliku)
  oraz `loading="lazy"` ręcznie.
- Obraz widoczny na pierwszym ekranie (LCP, np. portret na stronie głównej) ma `fetchpriority="high"` i **nie**
  ma `loading="lazy"`. Wszystko poniżej pierwszego ekranu ładuje się leniwie.
- Rozmiar: zwykle ≤ 1200 px szerokości i ≤ ~150 KB. Duże zdjęcia kompresuj przed dodaniem.
- Po zmianie istniejącego obrazu **zmień nazwę pliku lub dopisz `?v=` w `image`** (hosting cache’uje obrazy rok).
- Bez zewnętrznych czcionek, skryptów i widgetów ładowanych z cudzych domen bez wyraźnej potrzeby.

## 5. Dwie wersje językowe (PL/EN)

- Każda indeksowalna strona ma odpowiednik PL/EN z tym samym końcem adresu (np. `/artykuly/x/` ↔ `/en/articles/x/`).
- Nowy **typ** strony (nowy katalog) dopisz do pary w **dwóch** miejscach: `pairs` w `web/src/layouts/Base.astro`
  oraz `pairs` używane przez `counterpart()` w `web/astro.config.mjs`, a także do nawigacji i stopki w `Base.astro`.
  Bez tego znikną `hreflang` i alternatywy w sitemapie.
- Nowy wpis dodaj w obu kolekcjach (`src/content/...` i `src/content/en/...`), z tym samym slugiem i
  tłumaczeniem `title`, `description`, `imageAlt`.

## 6. Adresy, canonical, sitemapa, robots

- Adresy małymi literami, bez polskich znaków, z końcowym slashem (`trailingSlash: 'always'`). Raz nadanego adresu
  nie zmieniaj; jeśli musisz, dodaj przekierowanie 301 w `web/public/.htaccess`.
- Canonical (absolutny, `https://drmartakryczka.pl/...`), `hreflang`, Open Graph i Twitter generuje
  `Base.astro`: nie nadpisuj ich ręcznie.
- Sitemapa (`@astrojs/sitemap`) zawiera tylko strony indeksowalne i `lastmod`. Strona z `noindex` (np. 404) jest
  poza sitemapą. Nie dodawaj `noindex` do stron, które mają być w Google.
- Nowy plik w `public/` nie może kolidować z regułami `.htaccess` (410 dla `wp-*`, `feed`, `author`).

## 7. Dane strukturalne (JSON-LD)

- Szablon `Base.astro` dodaje `WebSite`, `Person` i `BreadcrumbList` (zgodny z hierarchią adresów i nawigacją);
  wpisy dodają `Article` z `author`, `datePublished`, `dateModified`, `image`.
- **Zabronione bez prawdziwych, weryfikowalnych opinii:** `Review`, `AggregateRating`. Nie dodajemy też `FAQPage`
  na siłę (Google nie pokazuje już FAQ rich results).
- Dane firmy (`LocalBusiness`/`Dentist`: adres, telefon, godziny) dopiero po otrzymaniu ich od Marty. Nic nie
  wymyślamy. `sameAs` tylko do prawdziwych, istniejących profili.
- Po zmianie: sprawdź wynik w [Rich Results Test](https://search.google.com/test/rich-results).

## 8. Wydajność i dostępność

- Cel Lighthouse (mobile) dla nowych stron: Wydajność ≥ 90, Dostępność 100, Najlepsze praktyki 100, SEO 100.
  Sprawdź lokalnie: `npx -y lighthouse https://drmartakryczka.pl/<adres>/ --only-categories=performance,accessibility,best-practices,seo`.
- Kontrast tekstu, widoczny focus, opisowe `aria-label` dla ikon i linków bez tekstu, atrybut `lang` zgodny z
  językiem strony.
- Linki zewnętrzne otwierane w nowej karcie mają `rel="noopener"`; linki do cudzych serwisów tylko tam, gdzie to
  potrzebne czytelnikowi.

## 9. Lista kontrolna przed publikacją

- [ ] `npm run build` przechodzi, a `python3 .github/scripts/seo_check.py` kończy się **0 błędów i 0 ostrzeżeń**.
- [ ] Unikalne `seoTitle` (≤ 41) i `seoDescription` (70–160), w PL i EN.
- [ ] Jeden H1, poprawna kolejność nagłówków, 2–3 linki wewnętrzne z opisowym tekstem.
- [ ] Zdjęcie/okładka z tego materiału, WebP, `alt` PL/EN, wymiary, nowa nazwa pliku po zmianie obrazu.
- [ ] Odpowiednik w drugiej wersji językowej i (dla nowego typu strony) wpis w `pairs` w dwóch plikach.
- [ ] Treść bez obietnic rezultatów i bez niepotwierdzonych danych; `updated` ustawione po zmianie treści.
- [ ] Wpis nie jest szkicem (`draft: false`) dopiero wtedy, gdy ma zdjęcie.

## 10. Po publikacji

1. Deploy zgłasza adresy do IndexNow (Bing i inne) automatycznie; krok jest „best effort” i nie blokuje wdrożenia.
2. **Google Search Console** (robi właściciel): „Zbadaj adres URL” → „Poproś o zindeksowanie” dla nowej strony;
   sitemapa `https://drmartakryczka.pl/sitemap-index.xml` powinna być dodana w sekcji „Mapy witryn”.
3. **Bing Webmaster Tools**: import strony z Google Search Console (jednorazowo).
4. Po 1–2 tygodniach sprawdź w GSC: indeksowanie, Core Web Vitals i zapytania; popraw title/description tam,
   gdzie CTR jest niski.
5. Linki zewnętrzne zdobywamy naturalnie (katalogi branżowe, wzmianki, współprace). Bez kupowania linków, PBN
   i wymian.
