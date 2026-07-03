# backend/app/services/notification_service.py
import asyncio
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    # In-memory storage for notifications
    _notifications: List[Dict] = []
    _subscribers: List[asyncio.Queue] = []
    
    @classmethod
    async def send_notification(cls, type: str, message: str, request_id: int):
        """Send notification to all subscribers"""
        notification = {
            "type": type,
            "message": message,
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store notification
        cls._notifications.append(notification)
        
        # Print to console
        print(f"\n{'='*50}")
        print(f"🔔 NOTIFICATION: {type.upper()}")
        print(f"   Message: {message}")
        print(f"   Request ID: {request_id}")
        print(f"   Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
        # Broadcast to all subscribers
        for queue in cls._subscribers:
            try:
                await queue.put(notification)
            except:
                pass
        
        return notification
    
    @classmethod
    async def subscribe(cls) -> asyncio.Queue:
        """Subscribe to notifications"""
        queue = asyncio.Queue()
        cls._subscribers.append(queue)
        return queue
    
    @classmethod
    def unsubscribe(cls, queue: asyncio.Queue):
        """Unsubscribe from notifications"""
        if queue in cls._subscribers:
            cls._subscribers.remove(queue)
    
    @classmethod
    def get_recent_notifications(cls, limit: int = 50):
        """Get recent notifications"""
        return cls._notifications[-limit:]