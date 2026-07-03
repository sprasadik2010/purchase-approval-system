import firebase_admin
from firebase_admin import credentials, messaging
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    _initialized = False
    
    @classmethod
    def initialize(cls):
        if not cls._initialized:
            try:
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                cls._initialized = True
                logger.info("Firebase initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase: {e}")
    
    @classmethod
    async def send_notification_to_user(cls, user_id: str, title: str, body: str, data: dict):
        cls.initialize()
        try:
            # In production, get FCM token from database
            # For demo, we'll use a topic
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data,
                topic="all"  # Use user-specific topic in production
            )
            response = messaging.send(message)
            logger.info(f"Notification sent: {response}")
            return response
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return None
    
    @classmethod
    async def get_user_notifications(cls, user_id: str):
        # In production, fetch from Firestore or database
        return [
            {
                "id": "1",
                "title": "Test Notification",
                "body": "This is a test notification",
                "data": {},
                "read": False,
                "timestamp": "2024-01-01T00:00:00"
            }
        ]
    
    @classmethod
    async def mark_notification_read(cls, notification_id: str):
        # Mark as read in database
        return True
