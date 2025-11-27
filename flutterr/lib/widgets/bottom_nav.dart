import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

class BottomNav extends StatelessWidget {
  final int currentIndex;
  final Function(int) onTap;

  const BottomNav({
    super.key,
    required this.currentIndex,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      constraints: const BoxConstraints(maxWidth: 480),
      margin: EdgeInsets.symmetric(
        horizontal: MediaQuery.of(context).size.width > 480
            ? (MediaQuery.of(context).size.width - 480) / 2
            : 0,
      ),
      decoration: BoxDecoration(
        color: AppColors.card,
        border: Border(
          top: BorderSide(color: AppColors.border, width: 1),
        ),
      ),
      child: BottomNavigationBar(
        currentIndex: currentIndex,
        onTap: onTap,
        backgroundColor: Colors.transparent,
        elevation: 0,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: AppColors.mutedForeground,
        selectedFontSize: 12,
        unselectedFontSize: 12,
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home, size: 24),
            label: 'Главная',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.work, size: 24),
            label: 'Услуги',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people, size: 24),
            label: 'Мастеры',
          ),
        ],
      ),
    );
  }
}

