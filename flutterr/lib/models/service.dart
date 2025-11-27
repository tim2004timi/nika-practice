class Service {
  final int id;
  final String title;
  final double price;
  final int durationQuarters;
  final int masterId;
  final String masterFullName;
  final String masterRole;
  final String masterPhoneNumber;

  Service({
    required this.id,
    required this.title,
    required this.price,
    required this.durationQuarters,
    required this.masterId,
    required this.masterFullName,
    required this.masterRole,
    required this.masterPhoneNumber,
  });

  // Helper getters for compatibility
  String get name => title;
  int get durationMinutes => durationQuarters * 30;
  String get masterName => masterFullName;
  String get masterType => masterRole;
  String get phone => masterPhoneNumber;

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id'],
      title: json['title'],
      price: double.parse(json['price']),
      durationQuarters: json['duration_quarters'],
      masterId: json['master_id'],
      masterFullName: json['master_full_name'],
      masterRole: json['master_role'],
      masterPhoneNumber: json['master_phone_number'],
    );
  }
}

