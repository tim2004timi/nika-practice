import 'package:intl/intl.dart';
import 'package:flutter/material.dart';

class Formatters {
  static String formatPrice(double price) {
    return '${price.toStringAsFixed(0)} ₽';
  }

  static String formatDuration(int minutes) {
    if (minutes < 60) {
      return '$minutes мин';
    }
    final hours = minutes ~/ 60;
    final mins = minutes % 60;
    if (mins == 0) {
      return '$hoursч';
    }
    return '$hoursч $mins мин';
  }

  static String formatDate(DateTime date) {
    return DateFormat('dd.MM').format(date);
  }

  static String formatTime(TimeOfDay time) {
    return '${time.hour.toString().padLeft(2, '0')}:${time.minute.toString().padLeft(2, '0')}';
  }

  static String formatDateForDisplay(DateTime date) {
    return DateFormat('dd.MM').format(date);
  }

  static String capitalize(String text) {
    if (text.isEmpty) return text;
    return text[0].toUpperCase() + text.substring(1);
  }
}

