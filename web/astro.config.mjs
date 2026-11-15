import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { satteri } from '@astrojs/markdown-satteri';
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

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

const root = dirname(fileURLToPath(import.meta.url));

function gitDate(file) {
  try {
    const out = execFileSync('git', ['log', '-1', '--format=%cI', '--', file], { cwd: root, encoding: 'utf8' }).trim();
    return out ? new Date(out) : null;
  } catch {
    return null;
  }
}

// Data ostatniej zmiany wpisów: `updated`, a w razie braku `date` z frontmattera.
function contentDates(dir, urlPrefix) {
  const dates = new Map();
  const abs = join(root, 'src/content', dir);
  if (!existsSync(abs)) return dates;
  for (const file of readdirSync(abs)) {
    if (!file.endsWith('.md')) continue;
    const text = readFileSync(join(abs, file), 'utf8');
    if (/^draft:\s*true/m.test(text)) continue;
    const pick = (key) => text.match(new RegExp(`^${key}:\\s*['"]?(\\d{4}-\\d{2}-\\d{2})`, 'm'))?.[1];
    const value = pick('updated') ?? pick('date');
    if (value) dates.set(`${urlPrefix}${file.replace(/\.md$/, '')}/`, new Date(value));
  }
  return dates;
}

const latest = (dates) => [...dates.values()].reduce((a, b) => (a > b ? a : b), new Date(0));
const entries = new Map([
  ...contentDates('artykuly', '/artykuly/'),
  ...contentDates('aktualnosci', '/aktualnosci/'),
  ...contentDates('en/artykuly', '/en/articles/'),
  ...contentDates('en/aktualnosci', '/en/news/'),
]);
const sectionLatest = (prefix) => latest(new Map([...entries].filter(([p]) => p.startsWith(prefix))));

function sourceFile(path) {
  const rel = path.replace(/^\/|\/$/g, '') || 'index';
  return [`src/pages/${rel}.astro`, `src/pages/${rel}/index.astro`].find((f) => existsSync(join(root, f)));
}

function lastmod(path) {
  if (entries.has(path)) return entries.get(path);
  const file = sourceFile(path);
  const own = file ? gitDate(file) : null;
  const newest = {
    '/': latest(entries),
    '/en/': latest(entries),
    '/artykuly/': sectionLatest('/artykuly/'),
    '/aktualnosci/': sectionLatest('/aktualnosci/'),
    '/en/articles/': sectionLatest('/en/articles/'),
    '/en/news/': sectionLatest('/en/news/'),
  }[path];
  if (!own) return newest ?? null;
  return newest && newest > own ? newest : own;
}

// Wymiary pliku WebP z nagłówka (VP8, VP8L, VP8X), żeby obrazy w treści miały width/height bez CLS.
function webpSize(file) {
  const b = readFileSync(file);
  if (b.toString('ascii', 0, 4) !== 'RIFF' || b.toString('ascii', 8, 12) !== 'WEBP') return null;
  const kind = b.toString('ascii', 12, 16);
  if (kind === 'VP8 ') return { width: b.readUInt16LE(26) & 0x3fff, height: b.readUInt16LE(28) & 0x3fff };
  if (kind === 'VP8L') {
    const bits = b.readUInt32LE(21);
    return { width: (bits & 0x3fff) + 1, height: ((bits >> 14) & 0x3fff) + 1 };
  }
  if (kind === 'VP8X') return { width: b.readUIntLE(24, 3) + 1, height: b.readUIntLE(27, 3) + 1 };
  return null;
}

// Obrazy w treści wpisów (markdown) ładują się leniwie, żeby nie konkurowały z elementem LCP.
const lazyImages = {
  name: 'lazy-images',
  element: {
    filter: ['img'],
    visit(node, ctx) {
      const src = node.properties?.src;
      ctx.setProperty(node, 'loading', 'lazy');
      ctx.setProperty(node, 'decoding', 'async');
      if (typeof src === 'string' && src.startsWith('/') && src.endsWith('.webp')) {
        const file = join(root, 'public', decodeURI(src));
        const size = existsSync(file) ? webpSize(file) : null;
        if (size) {
          ctx.setProperty(node, 'width', size.width);
          ctx.setProperty(node, 'height', size.height);
        }
      }
    },
  },
};

export default defineConfig({
  site,
  trailingSlash: 'always',
  markdown: { processor: satteri({ hastPlugins: [lazyImages] }) },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        const path = new URL(item.url).pathname;
        const modified = lastmod(path);
        if (modified && modified.getTime() > 0) item.lastmod = modified.toISOString();
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
