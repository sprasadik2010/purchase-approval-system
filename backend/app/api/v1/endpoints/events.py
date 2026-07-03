# backend/app/api/v1/endpoints/events.py
from fastapi.responses import StreamingResponse
import json
import asyncio
from app.services.notification_service import NotificationService

@router.get("/events/notifications")
async def stream_notifications():
    async def event_generator():
        queue = await NotificationService.subscribe()
        try:
            while True:
                notification = await queue.get()
                yield f"data: {json.dumps(notification)}\n\n"
        finally:
            NotificationService.unsubscribe(queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )