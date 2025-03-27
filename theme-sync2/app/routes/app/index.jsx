import { useEffect, useState } from "react";
import { useFetcher } from "@remix-run/react";

export default function AppHome() {
  const [themes, setThemes] = useState([]);
  const fetcher = useFetcher();

  useEffect(() => {
    const shop = new URLSearchParams(window.location.search).get("shop");
    if (!shop) return;

    fetch(`/fetch_themes?shop=${shop}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.themes) {
          setThemes(data.themes);
        } else {
          console.error("❌ Unexpected response:", data);
        }
      })
      .catch((err) => console.error("❌ Fetch error:", err));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>🎨 ThemeSync2 Dashboard</h1>
      <p>Below are the themes currently installed on this store:</p>
      <ul style={{ marginTop: "1rem" }}>
        {themes.length > 0 ? (
          themes.map((theme) => (
            <li key={theme.id}>
              <strong>{theme.name}</strong> – {theme.role}
            </li>
          ))
        ) : (
          <p>📭 No themes found yet, or loading...</p>
        )}
      </ul>
    </div>
  );
}
