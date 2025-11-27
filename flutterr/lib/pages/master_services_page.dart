import 'package:flutter/material.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_button.dart';
import '../services/data_service.dart';
import '../theme/app_colors.dart';
import '../models/master.dart';
import '../models/service.dart';
import '../utils/formatters.dart';
import 'service_detail_page.dart';

class MasterServicesPage extends StatefulWidget {
  final String masterId;

  const MasterServicesPage({super.key, required this.masterId});

  @override
  State<MasterServicesPage> createState() => _MasterServicesPageState();
}

class _MasterServicesPageState extends State<MasterServicesPage> {
  Master? _master;
  List<Service> _services = [];

  @override
  void initState() {
    super.initState();
    _loadMaster();
    _loadServices();
  }

  void _loadMaster() {
    final master = DataService.getMasterById(widget.masterId);
    setState(() {
      _master = master;
    });
  }

  void _loadServices() {
    final services = DataService.getServicesByMasterId(widget.masterId);
    setState(() {
      _services = services;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_master == null) {
      return Scaffold(
        body: Center(
          child: Text(
            'Мастер не найден',
            style: TextStyle(color: AppColors.mutedForeground),
          ),
        ),
      );
    }

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
              // Master info card
              CustomCard(
                padding: const EdgeInsets.all(24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _master!.name,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      Formatters.capitalize(_master!.type),
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
                          _master!.phone,
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
              // Services list
              const Text(
                'Услуги мастера',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 16),
              if (_services.isEmpty)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 32),
                  child: Center(
                    child: Text(
                      'Услуги не найдены',
                      style: TextStyle(
                        color: AppColors.mutedForeground,
                        fontSize: 16,
                      ),
                    ),
                  ),
                )
              else
                ..._services.map((service) {
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: CustomCard(
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => ServiceDetailPage(serviceId: service.id),
                          ),
                        );
                      },
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Expanded(
                            child: Text(
                              service.name,
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                          Text(
                            Formatters.formatPrice(service.price),
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: AppColors.primary,
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

