# app/main.py

from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="AI Co-worker Engine",
    description="Minimal interface for AI NPC collaboration",
    version="1.0"
)

app.include_router(router)