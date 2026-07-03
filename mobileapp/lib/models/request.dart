import 'package:flutter/material.dart';

class PurchaseRequest {
  final int id;
  final String title;
  final String? description;
  final String department;
  final String requestedBy;
  final double amount;
  final int quantity;
  final String unit;
  final String? vendor;
  final String priority;
  final String status;
  final String? notes;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? approvedBy;
  final DateTime? approvedAt;
  final String? rejectionReason;

  PurchaseRequest({
    required this.id,
    required this.title,
    this.description,
    required this.department,
    required this.requestedBy,
    required this.amount,
    required this.quantity,
    required this.unit,
    this.vendor,
    required this.priority,
    required this.status,
    this.notes,
    required this.createdAt,
    this.updatedAt,
    this.approvedBy,
    this.approvedAt,
    this.rejectionReason,
  });

  factory PurchaseRequest.fromJson(Map<String, dynamic> json) {
    return PurchaseRequest(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      department: json['department'],
      requestedBy: json['requested_by'],
      amount: json['amount'].toDouble(),
      quantity: json['quantity'],
      unit: json['unit'],
      vendor: json['vendor'],
      priority: json['priority'] ?? 'medium',
      status: json['status'],
      notes: json['notes'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
      approvedBy: json['approved_by'],
      approvedAt: json['approved_at'] != null ? DateTime.parse(json['approved_at']) : null,
      rejectionReason: json['rejection_reason'],
    );
  }

  bool get isPending => status == 'pending';
  bool get isApproved => status == 'approved';
  bool get isRejected => status == 'rejected';

  Color get statusColor {
    switch (status) {
      case 'pending':
        return Colors.orange;
      case 'approved':
        return Colors.green;
      case 'rejected':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  Color get priorityColor {
    switch (priority) {
      case 'high':
        return Colors.red;
      case 'medium':
        return Colors.orange;
      case 'low':
        return Colors.blue;
      default:
        return Colors.grey;
    }
  }
}