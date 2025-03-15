import os
import sys
import shutil
import zipfile
import sqlite3
import requests
import logging
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ✅ Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Ensure Python finds 'backend/'
sys.path.append(str(Path(__file__).resolve().parent))

# ✅ Load environment variables from .env file
dotenv_path = "C:\\Users\\Merri\\Documents\\Shopify-theme-tool\\backend\\.env"
if not load_dotenv(dotenv_path, override=True):
    raise RuntimeError(f"❌ Failed to load .env file! Looked in: {dotenv_path}")

# ✅ Shopify API Credentials
SHOPIFY_CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
SHOPIFY_CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")
SHOPIFY_REDIRECT_URI = os.getenv("SHOPIFY_REDIRECT_URI")
VITE_BACKEND_URL = os.getenv("VITE_BACKEND_URL", "http://localhost:8000")  # Fallback to localhost

if not SHOPIFY_CLIENT_ID or not SHOPIFY_CLIENT_SECRET or not SHOPIFY_REDIRECT_URI:
    raise ValueError("❌ ERROR: Missing Shopify API credentials in environment variables!")

logger.info("✅ Shopify API credentials loaded successfully.")

# ✅ Import API routes
try:
    from backend.themes import router as themes_router
except ModuleNotFoundError:
    from themes import router as themes_router

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ CORS Middleware Setup - Allow Shopify & Local Dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://village-digital-test.myshopify.com",
        "https://villagedigital-themesync.ngrok.app",
        VITE_BACKEND_URL,  # Ensure ngrok URL is dynamically loaded
        "http://localhost:8000",
    ],  # Allow Shopify, ngrok, and local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"✅ CORS configured for: https://village-digital-test.myshopify.com, {VITE_BACKEND_URL}, http://localhost:8000")

# ✅ Include the themes router
app.include_router(themes_router)

# ✅ Root Route (Fixes Shopify 404 Error)
@app.get("/")
def root():
    """Root route to confirm FastAPI is running & handle Shopify embedded app requests."""
    return {"message": "ThemeSync App is Running!"}

# ✅ Secure Access Token Storage (Using SQLite)
def store_access_token(shop, token):
    """Store the Shopify access token securely in SQLite."""
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tokens (shop TEXT PRIMARY KEY, access_token TEXT)")
    cursor.execute("INSERT OR REPLACE INTO tokens (shop, access_token) VALUES (?, ?)", (shop, token))
    conn.commit()
    conn.close()
    logger.info(f"✅ Access token stored securely for shop: {shop}")

def get_access_token(shop):
    """Retrieve the Shopify access token from SQLite."""
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT access_token FROM tokens WHERE shop = ?", (shop,))
    token = cursor.fetchone()
    conn.close()
    return token[0] if token else None

# ✅ Shopify OAuth - Redirect user to install app
@app.get("/auth")
def shopify_auth(shop: str = Query(..., description="Shopify store URL")):
    """Redirect the user to Shopify's OAuth authorization page."""
    auth_url = (
        f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_CLIENT_ID}"
        f"&scope=read_themes,write_themes&redirect_uri={SHOPIFY_REDIRECT_URI}&state=random_string"
    )
    return RedirectResponse(url=auth_url)

# ✅ Shopify OAuth Callback - Exchange code for access token
@app.get("/auth/callback")
def shopify_callback(code: str, shop: str):
    """Handle Shopify OAuth callback and exchange the code for an access token."""
    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": SHOPIFY_CLIENT_ID,
        "client_secret": SHOPIFY_CLIENT_SECRET,
        "code": code
    }

    try:
        response = requests.post(token_url, json=payload)
        response.raise_for_status()
        access_token = response.json().get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Access token not found in response")

        # ✅ Store access token securely
        store_access_token(shop, access_token)
        return {"message": "OAuth Success!", "access_token": access_token}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to get access token: {str(e)}")

# ✅ Shopify API - Fetch Themes
@app.get("/fetch_themes")
def fetch_shopify_themes(shop: str):
    """Fetch themes from a Shopify store using the stored access token."""
    access_token = get_access_token(shop)
    if not access_token:
        raise HTTPException(status_code=401, detail="❌ ERROR: No Shopify Access Token. Authenticate first!")

    headers = {"X-Shopify-Access-Token": access_token}
    url = f"https://{shop}/admin/api/2024-01/themes.json"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch themes: {str(e)}")

# ✅ Upload & Extract Shopify Themes
UPLOAD_DIR = Path("uploaded_themes")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload_theme/")
async def upload_theme(version: str, file: UploadFile = File(...)):
    """Upload and extract a theme ZIP file for comparison."""
    version_dir = UPLOAD_DIR / version

    # Remove existing directory before extraction
    if version_dir.exists():
        shutil.rmtree(version_dir)
    version_dir.mkdir(exist_ok=True)

    # Save the uploaded ZIP file
    zip_path = version_dir / file.filename
    try:
        with open(zip_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(version_dir)

        return {"message": f"Theme {version} uploaded and extracted successfully!"}

    except zipfile.BadZipFile:
        zip_path.unlink(missing_ok=True)  # Cleanup ZIP file
        raise HTTPException(status_code=400, detail="Invalid ZIP file. Extraction failed.")
    except Exception as e:
        zip_path.unlink(missing_ok=True)  # Cleanup ZIP file
        raise HTTPException(status_code=500, detail=f"Unexpected error during extraction: {str(e)}")
    finally:
        zip_path.unlink(missing_ok=True)  # Cleanup ZIP file after processing

# ✅ Root Route Confirmation for Debugging
@app.get("/status")
def status():
    """Check if the server is running correctly."""
    return {"status": "running", "message": "FastAPI backend is live!"}
