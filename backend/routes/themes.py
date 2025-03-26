from fastapi import APIRouter, Request
from utils.shopify_auth import get_shopify_client

router = APIRouter()

@router.get("/themes/files")
async def get_theme_files(request: Request):
    shop = request.query_params.get("shop")
    access_token = request.query_params.get("access_token")
    theme_id = request.query_params.get("theme_id")

    client = get_shopify_client(shop, access_token)

    query = """
    {
      theme(id: "gid://shopify/Theme/%s") {
        id
        name
        role
        themeStoreId
        createdAt
        updatedAt
        previewable
        processing
        files(first: 100) {
          edges {
            node {
              id
              key
              publicUrl
              createdAt
              updatedAt
            }
          }
        }
      }
    }
    """ % theme_id

    result = client.query(query)
    return result
