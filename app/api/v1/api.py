from fastapi import APIRouter
from app.api.v1.endpoints import menu, orders

api_router = APIRouter()

api_router.include_router(menu.router, prefix="/menu", tags=["Menu V1"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders V1"])