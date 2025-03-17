import { useEffect, useState } from "react";
import { Card } from "../ui/card"; // ✅ Corrected path
import { ScrollArea } from "@shadcn/ui";
import { Button } from "@/components/ui/button";
import { FolderOpen, FileText } from "lucide-react";

export default function ThemeFileExplorer() {
  // State for holding the fetched themes, selected theme, and files
  const [themes, setThemes] = useState([]);
  const [selectedTheme, setSelectedTheme] = useState(null);
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
  const SHOP = "village-digital-test.myshopify.com";

  // Fetch themes from the backend when the component is mounted
  useEffect(() => {
    fetch(`${BACKEND_URL}/fetch_themes?shop=${SHOP}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch themes");
        }
        return res.json();
      })
      .then((data) => {
        setThemes(data.themes || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Fetch files for a selected theme
  const fetchFiles = (themeId) => {
    setSelectedTheme(themeId);
    fetch(`${BACKEND_URL}/themes/files?theme_id=${themeId}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch theme files");
        }
        return res.json();
      })
      .then((data) => setFiles(data.files || []))
      .catch((err) => setError(err.message));
  };

  if (loading) return <div>Loading themes...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="flex h-screen w-full">
      {/* Sidebar: Theme Selection */}
      <aside className="w-1/4 bg-gray-100 p-4 border-r">
        <h2 className="text-lg font-semibold mb-3">Select a Theme</h2>
        <ScrollArea className="h-[calc(100vh-100px)]">
          {themes.map((theme) => (
            <Button
              key={theme.id}
              variant={selectedTheme === theme.id ? "default" : "outline"}
              className="w-full mb-2 flex items-center gap-2"
              onClick={() => fetchFiles(theme.id)}
            >
              <FolderOpen className="w-4 h-4" /> {theme.name}
            </Button>
          ))}
        </ScrollArea>
      </aside>

      {/* Main Panel: File Explorer */}
      <main className="flex-1 p-6">
        <h2 className="text-xl font-semibold mb-3">Theme Files</h2>
        <ScrollArea className="h-[calc(100vh-120px)] border p-4 rounded-lg">
          {files.length === 0 ? (
            <p className="text-gray-500">Select a theme to view files.</p>
          ) : (
            files.map((file) => (
              <Card key={file} className="p-2 mb-2 flex items-center gap-2">
                <FileText className="w-4 h-4 text-blue-500" /> {file}
              </Card>
            ))
          )}
        </ScrollArea>
      </main>
    </div>
  );
}
