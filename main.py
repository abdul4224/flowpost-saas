import os
import httpx
from fastapi import FastAPI, APIRouter, HTTPException, Request, status
from pydantic import BaseModel, HttpUrl
from typing import Optional

app = FastAPI(title="FlowPost AI Automation SaaS Engine")

# --- PHASE 2: WEBSITE ROUTING AUTOMATION ---
class ArticlePayload(BaseModel):
    title: str
    content: str
    meta_description: Optional[str] = None
    tags: Optional[list[str]] = []

@app.post("/api/v1/publish/web/wordpress")
async def publish_to_wordpress(payload: ArticlePayload):
    target_wp_url = "https://your-wordpress-site.com"
    wp_username = "admin_authorized"
    wp_app_password = "xxxx xxxx xxxx xxxx" # Enforced via env security keys
    
    headers = {"Content-Type": "application/json"}
    wp_data = {
        "title": payload.title,
        "content": payload.content,
        "status": "publish",
        "excerpt": payload.meta_description,
        "tags": payload.tags
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(target_wp_url, json=wp_data, auth=(wp_username, wp_app_password), headers=headers)
        if response.status_code != 201:
            raise HTTPException(status_code=400, detail="WordPress publishing engine breakdown.")
        return {"status": "Published", "platform": "WordPress", "post_id": response.json().get("id")}

# --- PHASE 3: SOCIAL MEDIA PIPELINE ---
class SocialPostPayload(BaseModel):
    caption: str
    media_url: Optional[str] = None
    hashtags: Optional[list[str]] = []

@app.post("/api/v1/publish/social/facebook/{page_id}")
async def post_to_facebook_page(page_id: str, payload: SocialPostPayload):
    page_access_token = "SECURE_PERMANENT_PAGE_ACCESS_TOKEN"
    fb_endpoint = f"https://facebook.com{page_id}/photos" if payload.media_url else f"https://facebook.com{page_id}/feed"
    
    post_params = {
        "url": payload.media_url if payload.media_url else None,
        "message": f"{payload.caption}\n\n{' '.join(payload.hashtags)}",
        "access_token": page_access_token
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(fb_endpoint, params=post_params)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Facebook Graph API network rejection.")
        return {"status": "Published", "platform": "Facebook Pages", "id": response.json().get("id")}
