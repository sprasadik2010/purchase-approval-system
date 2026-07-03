# backend/app/api/v1/endpoints/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from app.services.notification_service import NotificationService
import asyncio
import json

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    
    # Subscribe to notifications
    queue = await NotificationService.subscribe()
    
    try:
        while True:
            # Wait for notification
            notification = await queue.get()
            # Send to client
            await websocket.send_json(notification)
    except WebSocketDisconnect:
        # Unsubscribe on disconnect
        NotificationService.unsubscribe(queue)