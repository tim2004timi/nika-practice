class Service {
  final String id;
  final String name;
  final double price;
  final int durationMinutes;
  final String masterId;
  final String masterName;
  final String masterType;

  Service({
    required this.id,
    required this.name,
    required this.price,
    required this.durationMinutes,
    required this.masterId,
    required this.masterName,
    required this.masterType,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price': price,
      'durationMinutes': durationMinutes,
      'masterId': masterId,
      'masterName': masterName,
      'masterType': masterType,
    };
  }

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id'],
      name: json['name'],
      price: (json['price'] as num).toDouble(),
      durationMinutes: json['durationMinutes'],
      masterId: json['masterId'],
      masterName: json['masterName'],
      masterType: json['masterType'],
    );
  }
}

