import 'package:flutter/material.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_button.dart';
import '../services/api_service.dart';
import '../services/storage_service.dart';
import '../theme/app_colors.dart';
import '../models/service.dart';
import '../utils/formatters.dart';

class ServiceDetailPage extends StatefulWidget {
  final String serviceId;

  const ServiceDetailPage({super.key, required this.serviceId});

  @override
  State<ServiceDetailPage> createState() => _ServiceDetailPageState();
}

class _ServiceDetailPageState extends State<ServiceDetailPage> {
  Service? _service;
  DateTime _selectedDate = DateTime.now();
  int? _selectedQuarter;
  List<int> _freeQuarters = [];
  bool _isLoading = true;
  bool _isLoadingQuarters = false;

  @override
  void initState() {
    super.initState();
    _loadService();
  }

  Future<void> _loadService() async {
    setState(() {
      _isLoading = true;
    });
    try {
      final serviceId = int.parse(widget.serviceId);
      final service = await ApiService.getServiceById(serviceId);
      setState(() {
        _service = service;
        _isLoading = false;
      });
      _loadFreeQuarters();
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ошибка загрузки услуги: ${e.toString()}'),
            backgroundColor: AppColors.destructive,
          ),
        );
      }
    }
  }

  Future<void> _loadFreeQuarters() async {
    if (_service == null) return;
    
    setState(() {
      _isLoadingQuarters = true;
    });
    
    try {
      final dateStr = _formatDateForApi(_selectedDate);
      final quarters = await ApiService.getFreeQuarters(
        serviceId: _service!.id,
        date: dateStr,
      );
      setState(() {
        _freeQuarters = quarters;
        _isLoadingQuarters = false;
        // Reset selected quarter if it's not available
        if (_selectedQuarter != null && !quarters.contains(_selectedQuarter)) {
          _selectedQuarter = null;
        }
      });
    } catch (e) {
      setState(() {
        _isLoadingQuarters = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ошибка загрузки свободных кварталов: ${e.toString()}'),
            backgroundColor: AppColors.destructive,
          ),
        );
      }
    }
  }

  String _formatDateForApi(DateTime date) {
    return '${date.year}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
  }

  void _changeDate(int days) {
    final newDate = _selectedDate.add(Duration(days: days));
    final today = DateTime.now();
    if (newDate.isBefore(DateTime(today.year, today.month, today.day))) {
      return;
    }
    setState(() {
      _selectedDate = newDate;
      _selectedQuarter = null;
    });
    _loadFreeQuarters();
  }

  String _quarterToTime(int quarter) {
    // Quarter 1 = 8:00, each quarter = 30 minutes
    final startHour = 8;
    final quarters = quarter - 1;
    final totalMinutes = startHour * 60 + quarters * 30;
    final hours = totalMinutes ~/ 60;
    final minutes = totalMinutes % 60;
    return '${hours.toString().padLeft(2, '0')}:${minutes.toString().padLeft(2, '0')}';
  }

  List<int> _generateAllQuarters() {
    // 20 quarters from 8:00 to 17:30
    return List.generate(20, (index) => index + 1);
  }

  Future<void> _handleBooking() async {
    if (_selectedQuarter == null || _service == null) return;

    try {
      final clientId = await StorageService.getUserId();
      if (clientId == null) {
        throw Exception('Пользователь не авторизован');
      }

      final dateStr = _formatDateForApi(_selectedDate);
      await ApiService.createAppointment(
        clientId: clientId,
        serviceId: _service!.id,
        date: dateStr,
        quarter: _selectedQuarter!,
      );

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
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ошибка создания записи: ${e.toString()}'),
            backgroundColor: AppColors.destructive,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        body: Center(
          child: CircularProgressIndicator(color: AppColors.primary),
        ),
      );
    }

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

    final allQuarters = _generateAllQuarters();
    final today = DateTime.now();
    final canGoBack = _selectedDate.isAfter(DateTime(today.year, today.month, today.day));

    return Scaffold(
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () async {
            await _loadFreeQuarters();
          },
          color: AppColors.primary,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
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
                      _service!.masterFullName,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      Formatters.formatRole(_service!.masterRole),
                      style: TextStyle(
                        fontSize: 14,
                        color: AppColors.primary,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Icon(Icons.phone, size: 16, color: AppColors.mutedForeground),
                        const SizedBox(width: 8),
                        Text(
                          _service!.masterPhoneNumber,
                          style: TextStyle(
                            fontSize: 14,
                            color: AppColors.mutedForeground,
                          ),
                        ),
                      ],
                    ),
                    const Divider(height: 32, color: AppColors.border),
                    Text(
                      _service!.title,
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
              // Quarter selection
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
                  if (_isLoadingQuarters)
                    const Center(
                      child: Padding(
                        padding: EdgeInsets.all(16.0),
                        child: CircularProgressIndicator(),
                      ),
                    )
                  else
                    GridView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2,
                        crossAxisSpacing: 8,
                        mainAxisSpacing: 8,
                        childAspectRatio: 2.5,
                      ),
                      itemCount: allQuarters.length,
                      itemBuilder: (context, index) {
                        final quarter = allQuarters[index];
                        final isFree = _freeQuarters.contains(quarter);
                        final isSelected = _selectedQuarter == quarter;
                        final timeStr = _quarterToTime(quarter);

                        return CustomButton(
                          text: timeStr,
                          variant: isSelected
                              ? ButtonVariant.primary
                              : ButtonVariant.outline,
                          onPressed: isFree
                              ? () {
                                  setState(() {
                                    _selectedQuarter = quarter;
                                  });
                                }
                              : null,
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
      ),
      bottomNavigationBar: _selectedQuarter != null
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
