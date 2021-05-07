from fastapi import APIRouter
from .ws_chat import chat

ws_api = APIRouter()
ws_api.include_router(
    chat,
    prefix="/ws",
    tags=["WS_CHAT"]
)