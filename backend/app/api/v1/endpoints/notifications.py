# backend/app/api/v1/endpoints/notifications.py
from fastapi import APIRouter
from typing import List
from app.services.notification_service import NotificationService

router = APIRouter()

@router.get("/notifications/recent")
async def get_recent_notifications(limit: int = 50):
    """Get recent notifications (for polling)"""
    return NotificationService.get_recent_notifications(limit)

@router.get("/notifications/count")
async def get_notification_count():
    """Get count of notifications (for polling)"""
    return {"count": len(NotificationService._notifications)}