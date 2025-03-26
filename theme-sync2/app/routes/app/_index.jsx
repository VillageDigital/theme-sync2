import { Page, Layout, BlockStack, Card, Text, TitleBar } from "@shopify/polaris";

export default function AppHome() {
  return (
    <Page>
      <TitleBar title="ThemeSync2 Dashboard" />
      <BlockStack gap="500">
        <Layout>
          <Layout.Section>
            <Card>
              <BlockStack gap="400">
                <Text as="h2" variant="headingLg">
                  🎉 Welcome to ThemeSync2
                </Text>
                <Text as="p" variant="bodyMd">
                  This is your embedded app view inside Shopify. Everything is working.
                  Let’s build something beautiful. 🚀
                </Text>
              </BlockStack>
            </Card>
          </Layout.Section>
        </Layout>
      </BlockStack>
    </Page>
  );
}
