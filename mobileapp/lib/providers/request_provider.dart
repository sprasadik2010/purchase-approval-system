import 'package:flutter/material.dart';
import '../models/request.dart';
import '../services/api_service.dart';

class RequestProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  List<PurchaseRequest> _requests = [];
  bool _isLoading = false;
  String _error = '';

  List<PurchaseRequest> get requests => _requests;
  bool get isLoading => _isLoading;
  String get error => _error;

  Future<void> loadRequests() async {
    _isLoading = true;
    _error = '';
    notifyListeners();

    try {
      _requests = await _apiService.getRequests();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<PurchaseRequest?> getRequest(int id) async {
    try {
      return await _apiService.getRequest(id);
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return null;
    }
  }

  Future<void> createRequest(Map<String, dynamic> data) async {
    _isLoading = true;
    notifyListeners();

    try {
      final request = await _apiService.createRequest(data);
      _requests.insert(0, request);
    } catch (e) {
      _error = e.toString();
      rethrow;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> approveRequest(int id, {String? notes}) async {
    try {
      await _apiService.approveRequest(id, notes: notes);
      await loadRequests();
    } catch (e) {
      _error = e.toString();
      rethrow;
    }
  }

  Future<void> rejectRequest(int id, String reason) async {
    try {
      await _apiService.rejectRequest(id, reason);
      await loadRequests();
    } catch (e) {
      _error = e.toString();
      rethrow;
    }
  }

  List<PurchaseRequest> getFilteredRequests(String filter) {
    if (filter == 'all') return _requests;
    return _requests.where((r) => r.status == filter).toList();
  }

  Map<String, int> getStats() {
    return {
      'total': _requests.length,
      'pending': _requests.where((r) => r.status == 'pending').length,
      'approved': _requests.where((r) => r.status == 'approved').length,
      'rejected': _requests.where((r) => r.status == 'rejected').length,
    };
  }
}
