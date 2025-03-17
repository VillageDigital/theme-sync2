import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";  // ✅ This enables JSX support

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
  },
  optimizeDeps: {
    esbuildOptions: {
      loader: {
        ".js": "jsx", // ✅ This tells esbuild to treat .js files as JSX
      },
    },
  },
});
