import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/request.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  
  Future<List<PurchaseRequest>> getRequests({String? status}) async {
    final url = status != null ? '$baseUrl/purchase-requests/?status=$status' : '$baseUrl/purchase-requests/';
    final response = await http.get(Uri.parse(url));
    
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((item) => PurchaseRequest.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load requests');
    }
  }

  Future<PurchaseRequest> getRequest(int id) async {
    final response = await http.get(Uri.parse('$baseUrl/purchase-requests/$id'));
    
    if (response.statusCode == 200) {
      return PurchaseRequest.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load request');
    }
  }

  Future<PurchaseRequest> createRequest(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('$baseUrl/purchase-requests/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );
    
    if (response.statusCode == 201) {
      return PurchaseRequest.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create request');
    }
  }

  Future<void> approveRequest(int id, {String? notes, String approvedBy = 'Manager'}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/purchase-requests/$id/approve'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'approved_by': approvedBy,
        'notes': notes ?? '',
      }),
    );
    
    if (response.statusCode != 200) {
      throw Exception('Failed to approve request');
    }
  }

  Future<void> rejectRequest(int id, String reason, {String rejectedBy = 'Manager'}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/purchase-requests/$id/reject'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'reason': reason,
        'rejected_by': rejectedBy,
      }),
    );
    
    if (response.statusCode != 200) {
      throw Exception('Failed to reject request');
    }
  }
}