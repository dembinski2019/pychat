from fastapi import APIRouter, Request
from .routers import router

api = APIRouter()
api.include_router(
    router,
    prefix="/chat",
    tags=["chats"]
)

