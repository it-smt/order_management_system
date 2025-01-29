import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		watch: {
			usePolling: true,
		},
		host: true,
		strictPort: true,
		port: 5173,
	},
});
