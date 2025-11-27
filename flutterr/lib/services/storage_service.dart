import 'package:shared_preferences/shared_preferences.dart';

class StorageService {
  static const String _keyToken = 'accessToken';
  static const String _keyUserId = 'userId';
  static const String _keyUserName = 'userName';

  static Future<SharedPreferences> get _prefs async =>
      await SharedPreferences.getInstance();

  // Token management
  static Future<String?> getToken() async {
    final prefs = await _prefs;
    return prefs.getString(_keyToken);
  }

  static Future<void> setToken(String token) async {
    final prefs = await _prefs;
    await prefs.setString(_keyToken, token);
  }

  // User info
  static Future<bool> isAuthenticated() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  static Future<int?> getUserId() async {
    final prefs = await _prefs;
    return prefs.getInt(_keyUserId);
  }

  static Future<void> setUserId(int userId) async {
    final prefs = await _prefs;
    await prefs.setInt(_keyUserId, userId);
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
    await prefs.remove(_keyToken);
    await prefs.remove(_keyUserId);
    await prefs.remove(_keyUserName);
  }
}

