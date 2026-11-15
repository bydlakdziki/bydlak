# Strona dr Marty Kryczki

## Wdrożenie na home.pl

Workflow `.github/workflows/deploy.yml` publikuje `web/dist/` przez FTPS do `./marta/`
względem katalogu logowania konta FTP (`public_html`), czyli do `public_html/marta/`.
Domena `drmartakryczka.pl` powinna wskazywać ten katalog jako „Podkatalog z separacją serwisu”.
Strona pozostaje dostępna pod główną domeną, nie pod adresem `/marta/`.
Przy migracji najpierw wgraj pliki, następnie zmień przypisanie domeny w panelu home.pl
i sprawdź PL/EN, obrazy, rezerwacje oraz formularz PHP. Dotychczasowych plików
w głównym `public_html` nie usuwaj przed zakończeniem weryfikacji; pozwalają wycofać
zmianę przypisania domeny. Nie kieruj wdrożenia na katalog HotCast.

Statyczna strona w Astro: O mnie, Szkolenia, Zabiegi, Artykuły.

```bash
cd web
npm install
npm run dev      # podgląd lokalny
npm run build    # wynik w web/dist
```

- Nowe wydarzenie/konferencja: dodaj plik `.md` w `src/content/aktualnosci/` (wzór: `przyklad-wydarzenia.md`), zdjęcia w `public/img/aktualnosci/`, ustaw `draft: false`.
- Nowy artykuł: dodaj plik `.md` w `src/content/artykuly/` (wzór: `przyklad-artykulu.md`) i ustaw `draft: false`.
- Opcjonalne pola SEO we frontmatterze: `seoTitle` (maks. 41 znaków, tytuł w Google i breadcrumbach), `seoDescription` (maks. 160 znaków) oraz `updated` (data ostatniej zmiany, trafia do `dateModified`).
- Każdy publikowany artykuł i każda aktualność muszą mieć `image` oraz niepusty `imageAlt` w PL i EN; build blokuje publikację bez tych pól. Dla filmu używaj jego okładki lub kadru zapisanego lokalnie w `public/img/`. Bez dostępnego zdjęcia pozostaw `draft: true` do czasu otrzymania materiału.
- W aktualnościach opcjonalne `imageLink` ustawia adres filmu otwieranego po kliknięciu okładki we wpisie; uzupełnij go w PL i EN.
- Obrazy w treści `.md` dostają automatycznie `loading="lazy"`, `decoding="async"` oraz `width`/`height` (dla plików WebP z `public/`); plugin jest w `astro.config.mjs`. Używaj WebP.
- `lastmod` w sitemapie pochodzi z pola `updated`/`date` we wpisach, a dla stron statycznych z historii gita. Dlatego workflow deployu pobiera pełną historię (`fetch-depth: 0`).
- IndexNow (Bing): klucz jest w `public/<klucz>.txt`, a po deployu `.github/scripts/indexnow.py` zgłasza adresy z sitemapy (krok z `continue-on-error`). Po zmianie klucza zmień nazwę i treść pliku. Stronę trzeba samodzielnie dodać w Bing Webmaster Tools (import z Google Search Console).
- Favicony: `public/favicon.ico`, `favicon-192.png`, `apple-touch-icon.png`. Po zmianie ikony zmień nazwę pliku (hosting cache’uje obrazy przez rok).
- `public/.htaccess`: przekierowania do https i jednej domeny w jednym skoku, adresy katalogów ze slashem, kod 410 dla starych adresów WordPressa (`wp-*`, `feed`, `author`), kompresja i cache (CSS/JS rok, HTML bez cache).
- Certyfikaty i opis „O mnie”: edytuj `src/pages/o-mnie.astro`.
- Rezerwacje PL i EN na stronie głównej, w Zabiegach i Kontakcie: `src/components/BookingLinks.astro` (MEI Clinic / ZnanyLekarz oraz KG Instytut Dr Grudzień / Booksy).
- Portfolio (PL i EN): opisy i grupy zdjęć w `src/data/portfolio.ts`, zdjęcia w `public/img/portfolio/`. Dla każdego numeru slajdu dodaj `slide-N.webp` (1200 × 962) i `slide-N-small.webp` (640 × 513). Publikuj tylko materiały z udokumentowaną zgodą pacjenta na publikację na stronie; zachowuj oryginalne maskowanie oraz neutralne opisy bez obietnic rezultatów. Nie dodawaj źródłowej prezentacji do katalogu publicznego.
- Po wyborze domeny ustaw `site` w `astro.config.mjs`.
- Teksty oznaczone „Do uzupełnienia” wymagają danych zatwierdzonych przez Martę.
