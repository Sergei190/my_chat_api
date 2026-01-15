from fastapi import APIRouter
from app.api.v1 import chats, messages

v1_router = APIRouter()

v1_router.include_router(chats.router)
v1_router.include_router(messages.router)