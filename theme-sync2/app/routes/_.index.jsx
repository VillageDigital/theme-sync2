import { useEffect } from "react";
import { useFetcher } from "@remix-run/react";
import {
  Page,
  Layout,
  Text,
  Card,
  BlockStack,
  Box,
} from "@shopify/polaris";
import { TitleBar } from "@shopify/app-bridge-react";
import { authenticate } from "../shopify.server";

export const loader = async ({ request }) => {
  await authenticate.admin(request);
  return null;
};

export default function Index() {
  return (
    <Page>
      <TitleBar title="ThemeSync Dashboard" />
      <BlockStack gap="500">
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <Text as="h2" variant="headingLg">
                  🎉 Welcome to ThemeSync2
                </Text>
                <Text as="p" variant="bodyMd">
                  This is your Shopify theme optimization dashboard. Use the
                  tools in the sidebar to compare, merge, and sync themes.
                </Text>
                <Box padding="400" background="bg-surface-active" borderWidth="025" borderRadius="200" borderColor="border">
                  <div className="p-6 bg-gradient-to-r from-green-400 to-blue-500 text-white rounded-lg shadow">
                    <h2 className="text-2xl font-bold">🚀 Tailwind is working!</h2>
                    <p className="mt-2">This section is styled using TailwindCSS.</p>
                  </div>
                </Box>
              </BlockStack>
            </Card>
          </Layout.Section>
        </Layout>
      </BlockStack>
    </Page>
  );
}
