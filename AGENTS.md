# Publikowanie treści strony

- Każdy nowy artykuł i każda aktualność muszą mieć zdjęcie lub okładkę oraz opis alternatywny w obu wersjach językowych.
- Dla wpisu o filmie użyj okładki albo kadru z tego konkretnego filmu. Zapisz obraz lokalnie w `web/public/img/`, zamiast korzystać z wygasających adresów serwisów społecznościowych.
- Jeśli nie można pozyskać zdjęcia, pozostaw wpis jako szkic i poproś użytkownika o materiał. Nie publikuj wpisu bez zdjęcia ani z przypadkowym zamiennikiem.
- Po zmianie istniejącego zdjęcia zmień jego nazwę lub wersję w adresie `image`, ponieważ hosting buforuje obrazy przez rok. Dopasuj kadr do poziomej karty i sprawdź, czy twarz nie jest ucięta.

# SEO przy każdej zmianie na stronie

- Przy każdej nowej stronie, artykule, aktualności, obrazie, linku lub zmianie szablonu stosuj `docs/seo-najlepsze-praktyki.md` i przejdź jego listę kontrolną „przed publikacją”.
- Przed commitem zbuduj stronę i uruchom kontrolę: `cd web && npm run build && cd .. && python3 .github/scripts/seo_check.py`. Wynik ma być bez błędów i ostrzeżeń. Ta sama kontrola działa w pipeline: błędy blokują wdrożenie (`deploy.yml`) i pull request (`seo-check.yml`).
- Nowy typ strony wymaga wpisu w `pairs` w `web/src/layouts/Base.astro` i `web/astro.config.mjs` oraz odpowiednika PL/EN.
- Nie dodawaj `Review`/`AggregateRating`, obietnic rezultatów zabiegów ani niepotwierdzonych danych firmy.
