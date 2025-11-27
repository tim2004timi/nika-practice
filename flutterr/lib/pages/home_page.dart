import 'package:flutter/material.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_button.dart';
import '../services/storage_service.dart';
import '../theme/app_colors.dart';
import '../models/appointment.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String? _userName;
  List<Appointment> _appointments = [];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final userName = await StorageService.getUserName();
    final appointments = await StorageService.getAppointments();
    setState(() {
      _userName = userName ?? 'Пользователь';
      _appointments = appointments;
    });
  }

  Future<void> _handleLogout() async {
    await StorageService.clearAuth();
    if (mounted) {
      Navigator.of(context).pushReplacementNamed('/login');
    }
  }

  Future<void> _handleCancelAppointment(String id) async {
    await StorageService.removeAppointment(id);
    _loadData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Здравствуйте, $_userName',
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Ваши записи',
                          style: TextStyle(
                            fontSize: 14,
                            color: AppColors.mutedForeground,
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    onPressed: _handleLogout,
                    icon: const Icon(Icons.logout, size: 24),
                    color: AppColors.foreground,
                  ),
                ],
              ),
              const SizedBox(height: 24),
              if (_appointments.isEmpty)
                CustomCard(
                  padding: const EdgeInsets.all(32),
                  child: Center(
                    child: Column(
                      children: [
                        Text(
                          'У вас пока нет записей',
                          style: TextStyle(
                            color: AppColors.mutedForeground,
                            fontSize: 16,
                          ),
                        ),
                        const SizedBox(height: 16),
                        CustomButton(
                          text: 'Выбрать услугу',
                          onPressed: () {
                            Navigator.of(context).pushReplacementNamed('/services');
                          },
                          isFullWidth: false,
                        ),
                      ],
                    ),
                  ),
                )
              else
                ..._appointments.map((appointment) {
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 16),
                    child: CustomCard(
                      padding: const EdgeInsets.all(16),
                      child: Stack(
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(right: 32),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Text(
                                      appointment.date,
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w500,
                                        color: AppColors.primary,
                                      ),
                                    ),
                                    const SizedBox(width: 8),
                                    Text(
                                      'в',
                                      style: TextStyle(
                                        fontSize: 14,
                                        color: AppColors.mutedForeground,
                                      ),
                                    ),
                                    const SizedBox(width: 8),
                                    Text(
                                      appointment.time,
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w500,
                                        color: AppColors.primary,
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  appointment.serviceName,
                                  style: const TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  appointment.masterName,
                                  style: TextStyle(
                                    fontSize: 14,
                                    color: AppColors.mutedForeground,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Positioned(
                            top: 0,
                            right: 0,
                            child: IconButton(
                              onPressed: () => _handleCancelAppointment(appointment.id),
                              icon: const Icon(Icons.close, size: 18),
                              color: AppColors.mutedForeground,
                              padding: EdgeInsets.zero,
                              constraints: const BoxConstraints(),
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                }),
              const SizedBox(height: 80),
            ],
          ),
        ),
      ),
    );
  }
}

