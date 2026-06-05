import { defineConfig } from "vite";

export default defineConfig({
	build: {
		target: "esnext",
	},
	optimizeDeps: {
		exclude: ["svelte", "svelte/*"],
		esbuildOptions: {
			target: "esnext",
		},
	},
});
