class NotificationService {
  static Future<void> initialize() async {
    // Web doesn't support push notifications, just log
    print('Notification service initialized for web');
  }

  static Future<void> showNotification(String title, String body) async {
    // Show in console for web
    print('🔔 Notification: $title - $body');
  }
}