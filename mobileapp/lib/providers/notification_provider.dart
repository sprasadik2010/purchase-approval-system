import 'package:flutter/material.dart';

class NotificationProvider extends ChangeNotifier {
  int _notificationCount = 0;

  int get notificationCount => _notificationCount;

  void initializeNotifications() {
    // Simulate notifications for web
    _notificationCount = 0;
    notifyListeners();
  }

  void addNotification() {
    _notificationCount++;
    notifyListeners();
  }

  void clearNotifications() {
    _notificationCount = 0;
    notifyListeners();
  }
}