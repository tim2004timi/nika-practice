class User {
  final int id;
  final String login;
  final String fullName;
  final String phoneNumber;
  final String role;
  final String createdAt;

  User({
    required this.id,
    required this.login,
    required this.fullName,
    required this.phoneNumber,
    required this.role,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      login: json['login'],
      fullName: json['full_name'],
      phoneNumber: json['phone_number'],
      role: json['role'],
      createdAt: json['created_at'],
    );
  }
}

