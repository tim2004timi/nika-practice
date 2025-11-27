class Master {
  final int id;
  final String fullName;
  final String role;
  final String phoneNumber;
  final int servicesCount;

  Master({
    required this.id,
    required this.fullName,
    required this.role,
    required this.phoneNumber,
    required this.servicesCount,
  });

  // Helper getters for compatibility
  String get name => fullName;
  String get type => role;
  String get phone => phoneNumber;

  factory Master.fromJson(Map<String, dynamic> json) {
    return Master(
      id: json['id'],
      fullName: json['full_name'],
      role: json['role'],
      phoneNumber: json['phone_number'],
      servicesCount: json['services_count'] ?? 0,
    );
  }
}

