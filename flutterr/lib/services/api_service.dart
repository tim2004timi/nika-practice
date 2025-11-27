import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/auth_response.dart';
import '../models/user.dart';
import '../models/service.dart';
import '../models/master.dart';
import '../models/appointment.dart';
import 'storage_service.dart';

class ApiService {
  static const String baseUrl = 'http://37.9.13.207:8080';
  
  // Get authorization header
  static Future<Map<String, String>> _getHeaders({bool includeAuth = true}) async {
    final headers = <String, String>{
      'Content-Type': 'application/json',
    };
    
    if (includeAuth) {
      final token = await StorageService.getToken();
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }
    }
    
    return headers;
  }

  // Auth endpoints
  static Future<AuthResponse> register({
    required String login,
    required String password,
    required String fullName,
    required String phoneNumber,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/register'),
      headers: await _getHeaders(includeAuth: false),
      body: json.encode({
        'login': login,
        'password': password,
        'full_name': fullName,
        'phone_number': phoneNumber,
        'role': 'CLIENT',
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return AuthResponse.fromJson(json.decode(response.body));
    } else {
      throw Exception('Ошибка регистрации: ${response.body}');
    }
  }

  static Future<AuthResponse> login({
    required String username,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/token'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'username=$username&password=$password',
    );

    if (response.statusCode == 200) {
      return AuthResponse.fromJson(json.decode(response.body));
    } else {
      throw Exception('Ошибка входа: ${response.body}');
    }
  }

  static Future<User> getCurrentUser() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/users/me'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Ошибка получения пользователя: ${response.body}');
    }
  }

  // Masters endpoints
  static Future<List<Master>> getMasters() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/users/masters'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Master.fromJson(json)).toList();
    } else {
      throw Exception('Ошибка получения мастеров: ${response.body}');
    }
  }

  // Services endpoints
  static Future<List<Service>> getServices() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/services'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Service.fromJson(json)).toList();
    } else {
      throw Exception('Ошибка получения услуг: ${response.body}');
    }
  }

  static Future<List<Service>> getServicesByMasterId(int masterId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/services/masters/$masterId'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Service.fromJson(json)).toList();
    } else {
      throw Exception('Ошибка получения услуг мастера: ${response.body}');
    }
  }

  static Future<Service> getServiceById(int serviceId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/services/$serviceId'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      return Service.fromJson(json.decode(response.body));
    } else {
      throw Exception('Ошибка получения услуги: ${response.body}');
    }
  }

  static Future<List<int>> getFreeQuarters({
    required int serviceId,
    required String date, // YYYY-MM-DD
  }) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/services/$serviceId/free_quarters?date=$date'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final List<dynamic> quarters = data['free_quarters'];
      return quarters.map((q) => q as int).toList();
    } else {
      throw Exception('Ошибка получения свободных кварталов: ${response.body}');
    }
  }

  // Appointments endpoints
  static Future<List<Appointment>> getClientAppointments() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/appointments/client'),
      headers: await _getHeaders(),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Appointment.fromJson(json)).toList();
    } else {
      throw Exception('Ошибка получения записей: ${response.body}');
    }
  }

  static Future<Appointment> createAppointment({
    required int clientId,
    required int serviceId,
    required String date, // YYYY-MM-DD
    required int quarter,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/appointments'),
      headers: await _getHeaders(),
      body: json.encode({
        'client_id': clientId,
        'service_id': serviceId,
        'date': date,
        'quarter': quarter,
        'status': 'booked',
        'is_paid': false,
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return Appointment.fromJson(json.decode(response.body));
    } else {
      throw Exception('Ошибка создания записи: ${response.body}');
    }
  }

  static Future<void> deleteAppointment(int appointmentId) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/api/appointments/$appointmentId'),
      headers: await _getHeaders(),
    );

    if (response.statusCode != 204) {
      throw Exception('Ошибка удаления записи: ${response.body}');
    }
  }
}

