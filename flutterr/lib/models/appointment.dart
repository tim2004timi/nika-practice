class Appointment {
  final String id;
  final String date; // Format: "dd.MM"
  final String time; // Format: "HH:mm"
  final String serviceName;
  final String masterName;

  Appointment({
    required this.id,
    required this.date,
    required this.time,
    required this.serviceName,
    required this.masterName,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'date': date,
      'time': time,
      'serviceName': serviceName,
      'masterName': masterName,
    };
  }

  factory Appointment.fromJson(Map<String, dynamic> json) {
    return Appointment(
      id: json['id'],
      date: json['date'],
      time: json['time'],
      serviceName: json['serviceName'],
      masterName: json['masterName'],
    );
  }
}

