# Prompty do grafik strony – dr Marta Kryczka

Styl wspólny: spokojny, ciepły, premium, naturalne światło, paleta taupe `#5F452F`, piaskowy beż `#E9DDD0`, złamana biel `#FAF7F4`. Bez zębów w zbliżeniu, strzykawek, ludzi z widocznym wizerunkiem pacjentów i efektów „przed/po”.

**Ważne:** na stronę lekarza najlepiej dać **prawdziwe zdjęcia Marty** (sesja portretowa). Grafiki AI nadają się do teł i ilustracji, ale nie do wizerunku lekarza ani efektów zabiegów, bo mogą wprowadzać w błąd i naruszać zasady etyki lekarskiej. Obecne grafiki SVG w `web/public/` to tymczasowe, abstrakcyjne zamienniki.

## 1. Hero – tło / ilustracja (proporcje 4:5, 1600×2000)

```
Abstract elegant illustration for a doctor's personal website: a single thin continuous
line forming a soft face profile and gentle smile curve, on a warm sand-beige textured
background with soft overlapping circles. Muted taupe, sand and cream palette, calm,
premium, minimal, lots of negative space. No text, no realistic face, no medical symbols.
```

## 2. Tła kart sekcji (proporcje 5:3, 1200×720)

```
Soft abstract background with flowing thin taupe lines over a warm cream-to-sand
gradient, subtle paper texture, large pale circle in the corner. Calm minimalist
aesthetic-medicine brand mood. No text, no objects, no people.
```

## 3. O mnie – portret (do sesji lub generatora z własnym zdjęciem)

```
Editorial portrait of a confident, warm woman doctor in a white coat, soft natural window
light, neutral warm beige background, shallow depth of field, calm slight smile, natural
skin texture, premium healthcare brand photography, 4:5 vertical.
```

Uwaga: to prompt orientacyjny dla sesji. Na stronie użyj prawdziwego zdjęcia Marty, nie wygenerowanej postaci.

## 4. Szkolenia – wnętrze (16:9, 1920×1080)

```
Bright modern training room for doctors, a lecture table with an anatomy model and a
notebook, large window with soft natural light, warm neutral interior with beige and
taupe tones, no people, no visible faces, clean premium editorial photography.
```

## 5. Zabiegi – gabinet (16:9, 1920×1080)

```
Calm minimalist aesthetic medicine consultation room, a clean treatment chair, light
wood and warm beige textures, soft daylight, a small plant, no people, no syringes,
no products in focus, premium editorial interior photography.
```

## 6. Artykuły – okładki (16:9, 1600×900)

```
Flat lay on a warm beige surface: open notebook, pen, glasses and a small green plant,
soft diffused daylight from the side, muted taupe and cream tones, editorial photography,
space for text on the left, no text, no people.
```

## 7. Obraz udostępniania (Open Graph, 1200×630)

```
Warm sand-beige background with a thin taupe line face-profile symbol on the left and
empty space on the right for text, minimal, elegant, flat, premium brand look. No text.
```

## 8. O mnie – baner (16:9, 1920×1080, bez osób)

```
Elegant doctor's desk in warm daylight: framed certificates blurred in the background,
an open notebook, a fountain pen, a small olive plant and a cup of tea on a light wood
table, beige and taupe palette, soft natural window light, shallow depth of field,
calm and trustworthy atmosphere, premium editorial photography, space for text on the
left, no people, no readable text on the documents, no logos.
```

## 9. O mnie – tło pod własne zdjęcie Marty (4:5, 1600×2000)

```
Soft warm sand-beige studio backdrop with gentle window light and a subtle shadow of a
plant leaf on the wall, plain and uncluttered, space in the centre for a portrait, muted
taupe and cream tones, premium healthcare brand photography, no people, no text.
```

## 10. O mnie – ilustracja abstrakcyjna (spójna z hero, 4:5)

```
Minimal illustration in the same style as the website hero: thin taupe line art of
two hands gently holding a small leaf, on a warm sand-beige textured background with
soft overlapping circles, calm, feminine, premium, lots of negative space.
No text, no realistic faces, no medical symbols.
```

Na stronie „O mnie” najlepiej sprawdzi się prawdziwe zdjęcie Marty (sesja portretowa). Prompty 8–10 służą jako tło lub dodatek. Nie generuj certyfikatów ani dyplomów: dokumenty na stronie muszą być prawdziwe.

## Prompt negatywny

```
realistic patient face, before and after, syringe, needle, blood, teeth close-up, cartoon,
3D render, neon, clutter, text, watermark, logo of other brands, uncanny hands
```

## Gdzie wstawić pliki

- Hero: `web/public/hero.svg` (lub `.jpg` i zmiana ścieżki w `web/src/pages/index.astro`)
- Karty i nagłówki podstron: `web/public/karta.svg`
- Ikona karty: `web/public/favicon.svg` (docelowo monogram „MK” z logo)
- Zdjęcia zoptymalizuj przed wgraniem (WebP/JPG, do ok. 300 KB).
