# Strona dr Marty Kryczki

Statyczna strona w Astro: O mnie, Szkolenia, Zabiegi, Artykuły.

```bash
cd web
npm install
npm run dev      # podgląd lokalny
npm run build    # wynik w web/dist
```

- Nowe wydarzenie/konferencja: dodaj plik `.md` w `src/content/aktualnosci/` (wzór: `przyklad-wydarzenia.md`), zdjęcia w `public/img/aktualnosci/`, ustaw `draft: false`.
- Nowy artykuł: dodaj plik `.md` w `src/content/artykuly/` (wzór: `przyklad-artykulu.md`) i ustaw `draft: false`.
- Certyfikaty i opis „O mnie”: edytuj `src/pages/o-mnie.astro`.
- Rezerwacje PL i EN na stronie głównej, w Zabiegach i Kontakcie: `src/components/BookingLinks.astro` (MEI Clinic / ZnanyLekarz oraz KG Instytut Dr Grudzień / Booksy).
- Portfolio (PL i EN): opisy i grupy zdjęć w `src/data/portfolio.ts`, zdjęcia w `public/img/portfolio/`. Dla każdego numeru slajdu dodaj `slide-N.webp` (1200 × 962) i `slide-N-small.webp` (640 × 513). Publikuj tylko materiały z udokumentowaną zgodą pacjenta na publikację na stronie; zachowuj oryginalne maskowanie oraz neutralne opisy bez obietnic rezultatów. Nie dodawaj źródłowej prezentacji do katalogu publicznego.
- Po wyborze domeny ustaw `site` w `astro.config.mjs`.
- Teksty oznaczone „Do uzupełnienia” wymagają danych zatwierdzonych przez Martę.
