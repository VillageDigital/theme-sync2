from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# ✅ Load Shopify Access Token from environment variables
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

if not SHOPIFY_ACCESS_TOKEN:
    raise ValueError("❌ ERROR: Missing SHOPIFY_ACCESS_TOKEN in .env file!")

SHOPIFY_STORE_URL = "https://village-digital-test.myshopify.com"

@router.get("/themes/files")
def get_theme_files(theme_id: str):
    """
    Fetches the list of theme files from Shopify.
    """
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    url = f"{SHOPIFY_STORE_URL}/admin/api/2025-01/themes/{theme_id}/assets.json"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
