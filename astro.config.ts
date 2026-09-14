import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import tailwind from "@astrojs/tailwind";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
	site: "https://www.eveyhuang.com/",
	// Use ordinary browser navigation without speculative page requests.
	prefetch: false,
	redirects: {
		"/posts/coaching-model": "/posts/ai-coaching#understanding-coaching-expertise",
		"/posts/workplace-learning": "/posts/ai-coaching#learning-to-collaborate",
		"/posts/literary-style": "/posts/ai-coaching#early-work-on-tacit-judgment",
		"/posts/scientific-teams": "/posts/ai-team-science#scientific-teams",
		"/posts/entrepreneur-investor": "/posts/ai-team-science#entrepreneurinvestor-interaction",
		"/posts/volleyball-teams": "/posts/ai-team-science#professional-volleyball",
		"/posts/online-harassment": "/posts/double-compression#whose-judgments-shape-the-response",
	},
	markdown: {
		shikiConfig: {
			theme: "dracula",
			wrap: true,
		},
	},
	integrations: [
		mdx({}),
		tailwind({
			config: {
				applyBaseStyles: false,
			},
		}),
		sitemap(),
	],
	vite: {
		optimizeDeps: {
			exclude: ["@resvg/resvg-js"],
		},
	},
});
