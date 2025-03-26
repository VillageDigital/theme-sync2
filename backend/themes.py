from fastapi import APIRouter, HTTPException, Query
import requests
import sqlite3

router = APIRouter()

# ✅ Retrieve the access token from SQLite
def get_access_token(shop):
    """Retrieve access token from local SQLite database."""
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT access_token FROM tokens WHERE shop = ?", (shop,))
    token = cursor.fetchone()
    conn.close()
    return token[0] if token else None

# ✅ Endpoint to fetch theme files
@router.get("/themes/files")
def get_theme_files(shop: str = Query(...), theme_id: str = Query(...)):
    """
    Fetch the list of theme files from Shopify for a given shop and theme ID.
    """
    access_token = get_access_token(shop)
    if not access_token:
        raise HTTPException(status_code=401, detail="❌ No access token found. Please authenticate the shop first.")

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    url = f"https://{shop}/admin/api/2024-01/themes/{theme_id}/assets.json"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"❌ Failed to fetch theme files: {str(e)}")
