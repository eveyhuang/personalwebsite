import type { Config } from "tailwindcss";
import { fontFamily } from "tailwindcss/defaultTheme";
import plugin from "tailwindcss/plugin";

export default {
	content: ["./src/**/*.{astro,html,js,jsx,md,svelte,ts,tsx,vue}"],
	darkMode: "class",
	corePlugins: {
		aspectRatio: false,
		touchAction: false,
		ringOffsetWidth: false,
		ringOffsetColor: false,
		scrollSnapType: false,
		borderOpacity: false,
		textOpacity: false,
		fontVariantNumeric: false,
	},
	theme: {
		extend: {
			colors: {
				bgColor: "var(--theme-bg)",
				surface: "var(--theme-surface)",
				textColor: "var(--theme-text)",
				muted: "var(--theme-text-muted)",
				link: "var(--theme-link)",
				accent: "var(--theme-accent)",
				"accent-2": "var(--theme-accent-2)",
				line: "var(--theme-line)",
			},
			fontFamily: {
				sans: ["Space Grotesk", ...fontFamily.sans],
				serif: ["Newsreader", ...fontFamily.serif],
			},
			transitionProperty: {
				height: "height",
			},
			// eslint-disable-next-line @typescript-eslint/ban-ts-comment
			// @ts-ignore Tailwind exposes theme values at runtime.
			typography: (theme) => ({
				editorial: {
					css: {
						"--tw-prose-body": "var(--theme-text)",
						"--tw-prose-headings": "var(--theme-accent-2)",
						"--tw-prose-links": "var(--theme-link)",
						"--tw-prose-bold": "var(--theme-accent-2)",
						"--tw-prose-code": "var(--theme-accent-2)",
						"--tw-prose-bullets": "var(--theme-accent-2)",
						"--tw-prose-hr": "var(--theme-line)",
						maxWidth: "none",
						fontSize: theme("fontSize.base")[0],
						lineHeight: "1.75",
						a: {
							fontWeight: "500",
							textDecoration: "none",
							borderBottom: "1px solid var(--theme-line-strong)",
						},
						h2: {
							fontWeight: "600",
							letterSpacing: "-0.02em",
						},
						h3: {
							fontWeight: "600",
							letterSpacing: "-0.015em",
						},
						code: {
							border: "1px solid var(--theme-line)",
							borderRadius: "0.375rem",
							padding: "0.15rem 0.35rem",
						},
						"code::before": { content: "none" },
						"code::after": { content: "none" },
						blockquote: {
							fontStyle: "normal",
							borderInlineStart: "2px solid var(--theme-line-strong)",
							paddingInlineStart: "1rem",
						},
					},
				},
			}),
		},
	},
	plugins: [
		require("@tailwindcss/typography"),
		require("@tailwindcss/aspect-ratio"),
		plugin(function ({ addComponents }) {
			addComponents({
				".title": {
					"@apply text-3xl font-semibold text-accent-2": {},
				},
			});
		}),
	],
} satisfies Config;
