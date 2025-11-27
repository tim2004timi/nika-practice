import 'package:flutter/material.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_input.dart';
import '../services/data_service.dart';
import '../theme/app_colors.dart';
import '../models/service.dart';
import '../utils/formatters.dart';
import 'service_detail_page.dart';

class ServicesPage extends StatefulWidget {
  const ServicesPage({super.key});

  @override
  State<ServicesPage> createState() => _ServicesPageState();
}

class _ServicesPageState extends State<ServicesPage> {
  final _searchController = TextEditingController();
  final _priceFromController = TextEditingController();
  final _priceToController = TextEditingController();
  String _selectedMasterType = 'Все';
  List<Service> _allServices = [];
  List<Service> _filteredServices = [];

  @override
  void initState() {
    super.initState();
    _allServices = DataService.getServices();
    _filteredServices = _allServices;
    _searchController.addListener(_filterServices);
    _priceFromController.addListener(_filterServices);
    _priceToController.addListener(_filterServices);
  }

  @override
  void dispose() {
    _searchController.dispose();
    _priceFromController.dispose();
    _priceToController.dispose();
    super.dispose();
  }

  void _filterServices() {
    setState(() {
      final searchQuery = _searchController.text.toLowerCase();
      final masterType = _selectedMasterType;
      final priceFrom = _priceFromController.text.isNotEmpty
          ? double.tryParse(_priceFromController.text)
          : null;
      final priceTo = _priceToController.text.isNotEmpty
          ? double.tryParse(_priceToController.text)
          : null;

      _filteredServices = _allServices.where((service) {
        // Search filter
        if (searchQuery.isNotEmpty &&
            !service.name.toLowerCase().contains(searchQuery)) {
          return false;
        }

        // Master type filter
        if (masterType != 'Все' && service.masterType != masterType.toLowerCase()) {
          return false;
        }

        // Price filters
        if (priceFrom != null && service.price < priceFrom) {
          return false;
        }
        if (priceTo != null && service.price > priceTo) {
          return false;
        }

        return true;
      }).toList();
    });
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
              const Text(
                'Услуги',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 24),
              // Search
              CustomInput(
                hint: 'Поиск услуги...',
                controller: _searchController,
                prefixIcon: Icon(Icons.search, color: AppColors.mutedForeground, size: 20),
              ),
              const SizedBox(height: 16),
              // Filters
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Фильтры',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                      color: AppColors.foreground,
                    ),
                  ),
                  const SizedBox(height: 12),
                  // Master type filter
                  DropdownButtonFormField<String>(
                    initialValue: _selectedMasterType,
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: AppColors.card,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(6),
                        borderSide: BorderSide(color: AppColors.border),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(6),
                        borderSide: BorderSide(color: AppColors.border),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(6),
                        borderSide: BorderSide(color: AppColors.ring, width: 2),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 10,
                      ),
                    ),
                    dropdownColor: AppColors.popover,
                    style: TextStyle(color: AppColors.foreground),
                    items: const [
                      'Все',
                      'Визажист',
                      'Маникюрист',
                      'Стилист',
                      'Бровист',
                    ].map((type) {
                      return DropdownMenuItem(
                        value: type,
                        child: Text(type),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        _selectedMasterType = value!;
                      });
                      _filterServices();
                    },
                  ),
                  const SizedBox(height: 12),
                  // Price filters
                  Row(
                    children: [
                      Expanded(
                        child: CustomInput(
                          hint: 'Цена от',
                          controller: _priceFromController,
                          keyboardType: TextInputType.number,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: CustomInput(
                          hint: 'Цена до',
                          controller: _priceToController,
                          keyboardType: TextInputType.number,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              const SizedBox(height: 24),
              // Services list
              if (_filteredServices.isEmpty)
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
                ..._filteredServices.map((service) {
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
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
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
                          const SizedBox(height: 8),
                          Text(
                            service.masterName,
                            style: TextStyle(
                              fontSize: 14,
                              color: AppColors.mutedForeground,
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

