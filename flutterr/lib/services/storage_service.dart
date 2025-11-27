import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/appointment.dart';

class StorageService {
  static const String _keyIsAuthenticated = 'isAuthenticated';
  static const String _keyUserName = 'userName';
  static const String _keyAppointments = 'appointments';

  static Future<SharedPreferences> get _prefs async =>
      await SharedPreferences.getInstance();

  // Authentication
  static Future<bool> isAuthenticated() async {
    final prefs = await _prefs;
    return prefs.getString(_keyIsAuthenticated) == 'true';
  }

  static Future<void> setAuthenticated(bool value) async {
    final prefs = await _prefs;
    if (value) {
      await prefs.setString(_keyIsAuthenticated, 'true');
    } else {
      await prefs.remove(_keyIsAuthenticated);
    }
  }

  static Future<String?> getUserName() async {
    final prefs = await _prefs;
    return prefs.getString(_keyUserName);
  }

  static Future<void> setUserName(String userName) async {
    final prefs = await _prefs;
    await prefs.setString(_keyUserName, userName);
  }

  static Future<void> clearAuth() async {
    final prefs = await _prefs;
    await prefs.remove(_keyIsAuthenticated);
    await prefs.remove(_keyUserName);
  }

  // Appointments
  static Future<List<Appointment>> getAppointments() async {
    final prefs = await _prefs;
    final appointmentsJson = prefs.getString(_keyAppointments);
    if (appointmentsJson == null) {
      return [];
    }
    try {
      final List<dynamic> decoded = json.decode(appointmentsJson);
      return decoded.map((json) => Appointment.fromJson(json)).toList();
    } catch (e) {
      return [];
    }
  }

  static Future<void> saveAppointments(List<Appointment> appointments) async {
    final prefs = await _prefs;
    final appointmentsJson = json.encode(
      appointments.map((a) => a.toJson()).toList(),
    );
    await prefs.setString(_keyAppointments, appointmentsJson);
  }

  static Future<void> addAppointment(Appointment appointment) async {
    final appointments = await getAppointments();
    appointments.add(appointment);
    await saveAppointments(appointments);
  }

  static Future<void> removeAppointment(String id) async {
    final appointments = await getAppointments();
    appointments.removeWhere((a) => a.id == id);
    await saveAppointments(appointments);
  }
}

