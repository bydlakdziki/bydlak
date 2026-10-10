import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

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
  }),
});

export const collections = { artykuly };
