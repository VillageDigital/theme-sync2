import React from "react";
import { AppProvider, Frame, Navigation } from "@shopify/polaris";

function App() {
  return (
    <AppProvider>
      <Frame
        navigation={
          <Navigation location="/">
            <Navigation.Section
              items={[
                { label: "Dashboard", url: "/" },
                { label: "Settings", url: "/settings" },
              ]}
            />
          </Navigation>
        }
      >
        <div className="App">
          <h1>ThemeSync Dashboard</h1>
        </div>
      </Frame>
    </AppProvider>
  );
}

export default App;

