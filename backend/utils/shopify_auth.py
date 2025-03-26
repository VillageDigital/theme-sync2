import requests
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv(override=True)

SHOPIFY_API_VERSION = "2024-01"

def get_shopify_client(shop: str):
    token = get_access_token(shop)
    if not token:
        raise HTTPException(status_code=401, detail="❌ No access token. Authenticate first.")

    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": token,
    }

    base_url = f"https://{shop}/admin/api/{SHOPIFY_API_VERSION}"
    return base_url, headers

def get_access_token(shop: str):
    import sqlite3
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT access_token FROM tokens WHERE shop = ?", (shop,))
    token = cursor.fetchone()
    conn.close()
    return token[0] if token else None
