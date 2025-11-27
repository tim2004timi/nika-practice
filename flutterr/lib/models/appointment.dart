class Appointment {
  final int id;
  final String date; // Format: "YYYY-MM-DD"
  final int quarter; // 1-20
  final String status; // "booked" | "in_progress" | "completed"
  final bool isPaid;
  final String masterFullName;
  final String serviceTitle;
  final double servicePrice;
  final String clientFullName;

  Appointment({
    required this.id,
    required this.date,
    required this.quarter,
    required this.status,
    required this.isPaid,
    required this.masterFullName,
    required this.serviceTitle,
    required this.servicePrice,
    required this.clientFullName,
  });

  // Helper getters for compatibility
  String get serviceName => serviceTitle;
  String get masterName => masterFullName;

  // Convert date from YYYY-MM-DD to dd.MM
  String get formattedDate {
    final parts = date.split('-');
    if (parts.length == 3) {
      return '${parts[2]}.${parts[1]}';
    }
    return date;
  }

  // Convert quarter to time string (HH:mm)
  String get formattedTime {
    final startHour = 8;
    final quarters = quarter - 1;
    final totalMinutes = startHour * 60 + quarters * 30;
    final hours = totalMinutes ~/ 60;
    final minutes = totalMinutes % 60;
    return '${hours.toString().padLeft(2, '0')}:${minutes.toString().padLeft(2, '0')}';
  }

  factory Appointment.fromJson(Map<String, dynamic> json) {
    return Appointment(
      id: json['id'],
      date: json['date'],
      quarter: json['quarter'],
      status: json['status'],
      isPaid: json['is_paid'],
      masterFullName: json['master_full_name'],
      serviceTitle: json['service_title'],
      servicePrice: double.parse(json['service_price']),
      clientFullName: json['client_full_name'],
    );
  }
}

