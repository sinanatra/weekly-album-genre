import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  base: './',
  define: {
    __BUILD_DATE__: JSON.stringify(new Date().toISOString()),
  },
  build: {
    outDir: 'dist',
  },
});
