import 'package:flutter/material.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_button.dart';
import '../services/data_service.dart';
import '../services/storage_service.dart';
import '../models/master.dart';
import '../theme/app_colors.dart';
import '../models/service.dart';
import '../models/appointment.dart';
import '../utils/formatters.dart';

class ServiceDetailPage extends StatefulWidget {
  final String serviceId;

  const ServiceDetailPage({super.key, required this.serviceId});

  @override
  State<ServiceDetailPage> createState() => _ServiceDetailPageState();
}

class _ServiceDetailPageState extends State<ServiceDetailPage> {
  Service? _service;
  Master? _master;
  DateTime _selectedDate = DateTime.now();
  String? _selectedTime;
  List<String> _bookedSlots = [];

  @override
  void initState() {
    super.initState();
    _loadService();
    _generateBookedSlots();
  }

  void _loadService() {
    final service = DataService.getServiceById(widget.serviceId);
    Master? master;
    if (service != null) {
      master = DataService.getMasterById(service.masterId);
    }
    setState(() {
      _service = service;
      _master = master;
    });
  }

  void _generateBookedSlots() {
    // Generate some random booked slots for demo
    final random = DateTime.now().millisecondsSinceEpoch % 5;
    _bookedSlots = [];
    for (int i = 0; i < random; i++) {
      final hour = 8 + (i * 2);
      _bookedSlots.add('${hour.toString().padLeft(2, '0')}:00');
    }
  }

  List<String> _generateTimeSlots() {
    final slots = <String>[];
    for (int hour = 8; hour < 18; hour++) {
      slots.add('${hour.toString().padLeft(2, '0')}:00');
      if (hour < 17) {
        slots.add('${hour.toString().padLeft(2, '0')}:30');
      }
    }
    return slots;
  }

  void _changeDate(int days) {
    final newDate = _selectedDate.add(Duration(days: days));
    final today = DateTime.now();
    if (newDate.isBefore(DateTime(today.year, today.month, today.day))) {
      return;
    }
    setState(() {
      _selectedDate = newDate;
      _selectedTime = null;
      _generateBookedSlots();
    });
  }

  Future<void> _handleBooking() async {
    if (_selectedTime == null || _service == null) return;

    final appointment = Appointment(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      date: Formatters.formatDate(_selectedDate),
      time: _selectedTime!,
      serviceName: _service!.name,
      masterName: _service!.masterName,
    );

    await StorageService.addAppointment(appointment);

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('Запись успешно создана'),
          backgroundColor: AppColors.primary,
          duration: const Duration(seconds: 2),
        ),
      );
      Navigator.of(context).pushNamedAndRemoveUntil('/', (route) => false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_service == null) {
      return Scaffold(
        body: Center(
          child: Text(
            'Услуга не найдена',
            style: TextStyle(color: AppColors.mutedForeground),
          ),
        ),
      );
    }

    final timeSlots = _generateTimeSlots();
    final today = DateTime.now();
    final canGoBack = _selectedDate.isAfter(DateTime(today.year, today.month, today.day));

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Back button
              CustomButton(
                text: 'Назад',
                variant: ButtonVariant.ghost,
                icon: Icons.chevron_left,
                onPressed: () => Navigator.of(context).pop(),
                isFullWidth: false,
              ),
              const SizedBox(height: 8),
              // Service info card
              CustomCard(
                padding: const EdgeInsets.all(24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _service!.masterName,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      Formatters.capitalize(_service!.masterType),
                      style: TextStyle(
                        fontSize: 14,
                        color: AppColors.primary,
                      ),
                    ),
                    const SizedBox(height: 16),
                    if (_master != null)
                      Row(
                        children: [
                          Icon(Icons.phone, size: 16, color: AppColors.mutedForeground),
                          const SizedBox(width: 8),
                          Text(
                            _master!.phone,
                            style: TextStyle(
                              fontSize: 14,
                              color: AppColors.mutedForeground,
                            ),
                          ),
                        ],
                      ),
                    const Divider(height: 32, color: AppColors.border),
                    Text(
                      _service!.name,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          Formatters.formatPrice(_service!.price),
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: AppColors.primary,
                          ),
                        ),
                        Text(
                          Formatters.formatDuration(_service!.durationMinutes),
                          style: TextStyle(
                            fontSize: 14,
                            color: AppColors.mutedForeground,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              // Date selection
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Выбор даты',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                      color: AppColors.foreground,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        onPressed: canGoBack ? () => _changeDate(-1) : null,
                        icon: const Icon(Icons.chevron_left, size: 24),
                        color: AppColors.foreground,
                      ),
                      SizedBox(
                        width: 80,
                        child: Text(
                          Formatters.formatDate(_selectedDate),
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      IconButton(
                        onPressed: () => _changeDate(1),
                        icon: const Icon(Icons.chevron_right, size: 24),
                        color: AppColors.foreground,
                      ),
                    ],
                  ),
                ],
              ),
              const SizedBox(height: 24),
              // Time selection
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Выбор времени',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                      color: AppColors.foreground,
                    ),
                  ),
                  const SizedBox(height: 16),
                  GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      crossAxisSpacing: 8,
                      mainAxisSpacing: 8,
                      childAspectRatio: 2.5,
                    ),
                    itemCount: timeSlots.length,
                    itemBuilder: (context, index) {
                      final time = timeSlots[index];
                      final isBooked = _bookedSlots.contains(time);
                      final isSelected = _selectedTime == time;

                      return CustomButton(
                        text: time,
                        variant: isSelected
                            ? ButtonVariant.primary
                            : ButtonVariant.outline,
                        onPressed: isBooked
                            ? null
                            : () {
                                setState(() {
                                  _selectedTime = time;
                                });
                              },
                        isFullWidth: false,
                      );
                    },
                  ),
                ],
              ),
              const SizedBox(height: 100),
            ],
          ),
        ),
      ),
      bottomNavigationBar: _selectedTime != null
          ? Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.card,
                border: Border(
                  top: BorderSide(color: AppColors.border, width: 1),
                ),
              ),
              child: SafeArea(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 480),
                  child: CustomButton(
                    text: 'Забронировать',
                    onPressed: _handleBooking,
                    isFullWidth: true,
                  ),
                ),
              ),
            )
          : null,
    );
  }
}

