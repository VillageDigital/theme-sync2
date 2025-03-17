import { AppProvider } from "@shopify/polaris";
import { NavigationMenu } from "@shopify/app-bridge-react";
import polarisStyles from "@shopify/polaris/build/esm/styles.css?url";
import ThemeFileExplorer from "../components/ThemeFileExplorer.jsx"; // ✅ Corrected path

export const links = () => [{ rel: "stylesheet", href: polarisStyles }];

export default function App() {
  return (
    <AppProvider>
      <NavigationMenu
        navigationLinks={[
          { label: "Home", destination: "/app" },
          { label: "Additional page", destination: "/app/additional" }
        ]}
      />
      <ThemeFileExplorer /> {/* ✅ Now correctly referenced */}
    </AppProvider>
  );
}




