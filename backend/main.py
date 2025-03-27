import os
import sys
import shutil
import zipfile
import sqlite3
import requests
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ✅ Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Add backend path for imports
sys.path.append(str(Path(__file__).resolve().parent))

# ✅ Load environment variables
load_dotenv(override=True)

# ✅ Validate critical env vars
required_env_vars = ["SHOPIFY_CLIENT_ID", "SHOPIFY_CLIENT_SECRET", "SHOPIFY_REDIRECT_URI"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise RuntimeError(f"❌ Missing required env vars: {', '.join(missing_vars)}")

SHOPIFY_CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
SHOPIFY_CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")
SHOPIFY_REDIRECT_URI = os.getenv("SHOPIFY_REDIRECT_URI")
VITE_BACKEND_URL = os.getenv("VITE_BACKEND_URL", "http://localhost:8000")

logger.info("✅ Shopify credentials loaded.")

# ✅ Import API routes
try:
    from routes.themes import router as themes_router
except ModuleNotFoundError:
    from routes.themes import router as themes_router

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Allow CORS for Shopify + ngrok + local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pixelmermaid-lab.myshopify.com",
        "https://village-digital-themesync.ngrok.app",
        VITE_BACKEND_URL,
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mounting Remix frontend is DISABLED (Shopify handles this)
# Do NOT mount /app or override Remix frontend paths here

# ✅ Root route → redirects Shopify to Remix app shell
@app.get("/")
def root_redirect():
    return RedirectResponse(url="/app")

# ✅ Health check
@app.get("/status")
def status():
    return {"status": "running", "message": "FastAPI backend is live!"}

# ✅ Include theme routes
app.include_router(themes_router)

# ✅ Token DB helpers
def store_access_token(shop, token):
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tokens (shop TEXT PRIMARY KEY, access_token TEXT)")
    cursor.execute("INSERT OR REPLACE INTO tokens (shop, access_token) VALUES (?, ?)", (shop, token))
    conn.commit()
    conn.close()

def get_access_token(shop):
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT access_token FROM tokens WHERE shop = ?", (shop,))
    token = cursor.fetchone()
    conn.close()
    return token[0] if token else None

# ✅ OAuth start
@app.get("/auth")
def shopify_auth(shop: str = Query(...)):
    auth_url = (
        f"https://{shop}/admin/oauth/authorize"
        f"?client_id={SHOPIFY_CLIENT_ID}"
        f"&scope=read_themes,write_themes,write_products"
        f"&redirect_uri={SHOPIFY_REDIRECT_URI}"
        f"&state=random_string"
    )
    return RedirectResponse(url=auth_url)

# ✅ OAuth callback
@app.get("/auth/callback")
def shopify_callback(code: str, shop: str):
    token_url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": SHOPIFY_CLIENT_ID,
        "client_secret": SHOPIFY_CLIENT_SECRET,
        "code": code,
    }

    try:
        response = requests.post(token_url, json=payload)
        response.raise_for_status()
        access_token = response.json().get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Access token not found")

        store_access_token(shop, access_token)

        return RedirectResponse(url="https://admin.shopify.com/store/pixelmermaid-lab/apps/themesync2")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to get token: {str(e)}")

# ✅ Fetch themes
@app.get("/fetch_themes")
def fetch_shopify_themes(shop: str):
    access_token = get_access_token(shop)
    if not access_token:
        raise HTTPException(status_code=401, detail="❌ No token found. Authenticate first.")

    headers = {"X-Shopify-Access-Token": access_token}
    url = f"https://{shop}/admin/api/2024-01/themes.json"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch themes: {str(e)}")

# ✅ Upload theme ZIP files
UPLOAD_DIR = Path("uploaded_themes")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload_theme/")
async def upload_theme(version: str, file: UploadFile = File(...)):
    version_dir = UPLOAD_DIR / version
    version_dir.mkdir(parents=True, exist_ok=True)

    file_path = version_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "✅ Upload successful", "version": version, "filename": file.filename}

# ✅ Handle /app route for Shopify iframe loading
@app.get("/app")
def serve_app_shell():
    return {"message": "ThemeSync2 app shell is live."}
