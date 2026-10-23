import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const hasPublishedCover = (entry: { draft: boolean; image?: string; imageAlt: string }) =>
  entry.draft || Boolean(entry.image?.trim() && entry.imageAlt.trim());
const coverRequired = {
  message: 'Published articles and news require an image and imageAlt.',
  path: ['image'],
};

const artykuly = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/artykuly' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    category: z.string(),
    image: z.string().optional(),
    imageAlt: z.string().default(''),
    draft: z.boolean().default(false),
  }).refine(hasPublishedCover, coverRequired),
});

const aktualnosci = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/aktualnosci' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    type: z.string().default('Wydarzenie'),
    location: z.string().optional(),
    link: z.string().url().optional(),
    imageLink: z.string().url().optional(),
    image: z.string().optional(),
    imageAlt: z.string().default(''),
    draft: z.boolean().default(false),
  }).refine(hasPublishedCover, coverRequired),
});

const artykulyEn = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/en/artykuly' }),
  schema: artykuly.schema,
});
const aktualnosciEn = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/en/aktualnosci' }),
  schema: aktualnosci.schema,
});

export const collections = { artykuly, aktualnosci, 'artykuly-en': artykulyEn, 'aktualnosci-en': aktualnosciEn };
