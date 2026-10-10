import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://drmartakryczka.pl',
  trailingSlash: 'always',
  integrations: [sitemap({ filter: (page) => !page.includes('/404'), i18n: { defaultLocale: 'pl', locales: { pl: 'pl-PL', en: 'en-GB' } } })],
});
