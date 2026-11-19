# CLAUDE.md – strona dr Marty Kryczki (drmartakryczka.pl)

Statyczna, dwujęzyczna (PL/EN) strona w Astro 7 (Node 22). Treści i dokumenty po polsku – odpowiadaj po polsku.
Instrukcje z `AGENTS.md` (oryginał z czasów Copilota) są włączone poniżej; szczegóły operacyjne: `web/README.md`.

## Mapa repo

- `web/` – cała strona (Astro). `web/package.json`: skrypty `dev`, `build`, `preview` (brak testów i lintera).
  - `src/pages/` – strony PL (`o-mnie`, `szkolenia`, `zabiegi`, `portfolio`, `kontakt`, `aktualnosci/`, `artykuly/`, `404`) i EN w `src/pages/en/` (`about`, `training`, `treatments`, `portfolio`, `contact`, `news/`, `articles/`).
  - `src/content/{aktualnosci,artykuly}/` – wpisy PL w Markdown; EN w `src/content/en/{aktualnosci,artykuly}/`. Schemat (frontmatter) w `src/content.config.ts`.
  - `src/components/` (m.in. `BookingLinks.astro`, `Portfolio.astro`), `src/layouts/Base.astro`, `src/data/portfolio.ts`, `src/styles/global.css`.
  - `public/` – statyki: `img/`, `.htaccess` w deployu, `wyslij.php` (formularz kontaktowy), `robots.txt`, favicony, plik klucza IndexNow (`<klucz>.txt`).
  - `astro.config.mjs` – `site`, sitemap (hreflang PL↔EN przez `pairs`, `lastmod`), plugin obrazów w Markdown.
- `docs/` – SEO (`seo-najlepsze-praktyki.md`), strategia marki, Instagram, prompty grafik/logo.
- `.github/scripts/` – `seo_check.py` (kontrola zbudowanej strony `web/dist`), `indexnow.py` (zgłoszenie URL-i po deployu).
- `.github/workflows/`:
  - `deploy.yml` – push na `master` (ścieżki `web/**`): `npm ci` → `npm run build` → `seo_check.py` → FTPS do `./marta/` (home.pl) → IndexNow (`continue-on-error`). Wymaga `fetch-depth: 0` (daty sitemapy z gita).
  - `seo-check.yml` – PR dotykające `web/**`, skryptu lub docs SEO: build + `seo_check.py`.
  - `ftp-check.yml` – ręczny, tylko odczyt FTPS (diagnostyka). Sekrety `FTP_SERVER`/`FTP_USERNAME`/`FTP_PASSWORD` są tylko w GitHub Secrets.

## Polecenia (zweryfikowane: build i kontrola SEO przechodzą, 41 stron, 0 błędów, 0 ostrzeżeń)

```bash
cd web && npm ci            # instalacja (CI używa npm ci)
npm run dev                 # podgląd lokalny
npm run build               # wynik w web/dist
cd .. && python3 .github/scripts/seo_check.py   # kontrola SEO po buildzie (z roota repo)
```

Jedno polecenie przed commitem: `cd web && npm run build && cd .. && python3 .github/scripts/seo_check.py` – wynik ma być **bez błędów i ostrzeżeń**.
Testów jednostkowych ani lintera brak.

## Zasady (z AGENTS.md i web/README.md)

**Publikowanie treści**
- Każdy artykuł i aktualność: zdjęcie/okładka (`image`) oraz niepusty `imageAlt` w wersji PL **i** EN (build blokuje publikację bez tego; `draft: true` zwalnia z wymogu).
- Wpis o filmie: okładka lub kadr z tego filmu, zapisany lokalnie w `web/public/img/` (nie linkuj wygasających adresów social media). Brak zdjęcia → zostaw `draft: true` i poproś użytkownika o materiał; nie publikuj z przypadkowym zamiennikiem.
- Zmiana istniejącego zdjęcia → zmień nazwę/wersję w `image` (hosting cache'uje obrazy rok). Kadr dopasuj do poziomej karty, nie ucinaj twarzy. Używaj WebP.
- Nowy wpis: skopiuj wzór (`przyklad-artykulu.md` / `przyklad-wydarzenia.md`), ustaw `draft: false`. Pola SEO: `seoTitle` ≤ 41 znaków, `seoDescription` ≤ 160, opcjonalnie `updated`. W aktualnościach `imageLink` (adres filmu) uzupełnij w PL i EN.
- Portfolio: `src/data/portfolio.ts`, zdjęcia `public/img/portfolio/slide-N.webp` (1200×962) i `slide-N-small.webp` (640×513). Tylko materiały z udokumentowaną zgodą pacjenta, zachowuj maskowanie, opisy neutralne, bez obietnic rezultatów; nie dodawaj źródłowej prezentacji do katalogu publicznego.
- Teksty „Do uzupełnienia” wymagają danych zatwierdzonych przez Martę.

**SEO**
- Przy każdej nowej stronie/artykule/aktualności/obrazie/linku/zmianie szablonu przejdź listę „przed publikacją” z `docs/seo-najlepsze-praktyki.md`.
- Nowy typ strony → wpis w `pairs` w **obu** plikach: `web/src/layouts/Base.astro` i `web/astro.config.mjs`, plus odpowiednik PL/EN.
- Nie dodawaj `Review`/`AggregateRating`, obietnic rezultatów zabiegów ani niepotwierdzonych danych firmy.

## Pułapki

- Deploy idzie wyłącznie z `master` do `public_html/marta/` (nie na katalog HotCast); nie usuwaj dotychczasowych plików z głównego `public_html` przed weryfikacją migracji domeny.
- `seo_check.py` uruchamiaj po buildzie, z `web/dist` – bez buildu nie ma czego sprawdzać. Lokalnie jest Python 3.9 (skrypt przeszedł).
- Daty `lastmod` stron statycznych biorą się z historii gita – płytki klon może je zaburzyć.
- Po zmianie klucza IndexNow zmień nazwę i treść pliku `web/public/<klucz>.txt`; po zmianie favicon zmień nazwę pliku.
- `wyslij.php` zawiera adres odbiorcy formularza; nie dodawaj do repo żadnych haseł ani kluczy.
- `site` w `astro.config.mjs` to `https://drmartakryczka.pl`.
- `web/node_modules`, `web/dist`, `.astro` są w `.gitignore`.
- Brak w repo `.github/skills` i `.github/copilot-instructions.md` – nie ma skilli do przeniesienia; jedyne instrukcje agenta to `AGENTS.md` (zostaje bez zmian).
