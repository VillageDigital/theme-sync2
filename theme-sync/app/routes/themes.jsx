import { useEffect, useState } from "react";

export default function ThemeFileExplorer() {
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const SHOPIFY_STORE = "village-digital-test.myshopify.com"; // Your Shopify store name

  useEffect(() => {
    fetch(`https://24ef2e01b45a.ngrok.app/fetch_themes?shop=${SHOPIFY_STORE}`)
      .then((res) => res.json())
      .then((data) => {
        setThemes(data.themes || []);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching themes:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold mb-3">Shopify Themes</h2>

      {loading ? (
        <p>Loading themes...</p>
      ) : themes.length === 0 ? (
        <p>No themes found.</p>
      ) : (
        <ul className="border rounded-lg p-4">
          {themes.map((theme) => (
            <li key={theme.id} className="p-2 border-b">
              <strong>{theme.name}</strong> (ID: {theme.id})
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

