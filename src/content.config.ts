import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Indsigt = short articles/news. One Markdown file per post in src/content/indsigt/.
const indsigt = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/indsigt" }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(200),
    date: z.coerce.date(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { indsigt };
