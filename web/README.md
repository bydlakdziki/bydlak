# Strona dr Marty Kryczki

Statyczna strona w Astro: O mnie, Szkolenia, Zabiegi, Artykuły.

```bash
cd web
npm install
npm run dev      # podgląd lokalny
npm run build    # wynik w web/dist
```

- Nowy artykuł: dodaj plik `.md` w `src/content/artykuly/` (wzór: `przyklad-artykulu.md`) i ustaw `draft: false`.
- Certyfikaty i opis „O mnie”: edytuj `src/pages/o-mnie.astro`.
- Po wyborze domeny ustaw `site` w `astro.config.mjs`.
- Teksty oznaczone „Do uzupełnienia” wymagają danych zatwierdzonych przez Martę.
