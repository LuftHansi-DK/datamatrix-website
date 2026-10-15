import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://www.datamatrix.dk",
  trailingSlash: "always",
  integrations: [sitemap({ filter: (page) => !page.includes("/v/") && !page.includes("/looks/") })],
});
