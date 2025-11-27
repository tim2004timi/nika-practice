class Master {
  final String id;
  final String name;
  final String type;
  final String phone;

  Master({
    required this.id,
    required this.name,
    required this.type,
    required this.phone,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'type': type,
      'phone': phone,
    };
  }

  factory Master.fromJson(Map<String, dynamic> json) {
    return Master(
      id: json['id'],
      name: json['name'],
      type: json['type'],
      phone: json['phone'],
    );
  }
}

