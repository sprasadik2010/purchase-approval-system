from fastapi import APIRouter
from .endpoints import purchase_requests, notifications

router = APIRouter()
router.include_router(purchase_requests.router, prefix="/purchase-requests", tags=["purchase-requests"])
router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
