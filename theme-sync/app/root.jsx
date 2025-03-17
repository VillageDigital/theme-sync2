import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  LiveReload
} from "@remix-run/react";
import polarisStyles from "@shopify/polaris/build/esm/styles.css?url";

export const links = () => [
  { rel: "preconnect", href: "https://cdn.shopify.com/" },
  { rel: "stylesheet", href: "https://cdn.shopify.com/static/fonts/inter/v4/styles.css" },
  { rel: "stylesheet", href: polarisStyles }
];

export const meta = () => [
  { title: "ThemeSync App - Village Digital" },
];

export default function App() {
  return (
    <html lang="en">
      <head>
        <Meta />
        <Links />
      </head>
      <body className="bg-gray-100 text-gray-900">
        <nav className="p-4 bg-white shadow">
          <a
            href="/app"
            style={{
              fontWeight: 'bold',
              color: '#2B2D42',
              textDecoration: 'none'
            }}
          >
            Open Theme File Explorer
          </a>
        </nav>

        <main className="p-6">
          <Outlet />
        </main>

        <ScrollRestoration />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
}

