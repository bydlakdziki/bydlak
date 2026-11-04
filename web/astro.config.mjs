import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const site = 'https://drmartakryczka.pl';
const pairs = [
  ['/o-mnie/', '/en/about/'],
  ['/szkolenia/', '/en/training/'],
  ['/zabiegi/', '/en/treatments/'],
  ['/portfolio/', '/en/portfolio/'],
  ['/aktualnosci/', '/en/news/'],
  ['/artykuly/', '/en/articles/'],
  ['/kontakt/', '/en/contact/'],
];

// Podstrony PL i EN mają różne ścieżki, więc pary hreflang wyznaczamy ręcznie.
function counterpart(path) {
  if (path === '/') return '/en/';
  if (path === '/en/') return '/';
  for (const [pl, en] of pairs) {
    if (path.startsWith(pl)) return en + path.slice(pl.length);
    if (path.startsWith(en)) return pl + path.slice(en.length);
  }
  return null;
}

export default defineConfig({
  site,
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        const path = new URL(item.url).pathname;
        const other = counterpart(path);
        if (other) {
          const isEn = path.startsWith('/en/');
          const pl = isEn ? other : path;
          const en = isEn ? path : other;
          item.links = [
            { url: site + pl, lang: 'pl-PL' },
            { url: site + en, lang: 'en-GB' },
          ];
        }
        return item;
      },
    }),
  ],
});
