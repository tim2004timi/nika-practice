import 'package:flutter/material.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_input.dart';
import '../services/data_service.dart';
import '../theme/app_colors.dart';
import '../models/master.dart';
import '../models/service.dart';
import '../utils/formatters.dart';
import 'master_services_page.dart';

class MastersPage extends StatefulWidget {
  const MastersPage({super.key});

  @override
  State<MastersPage> createState() => _MastersPageState();
}

class _MastersPageState extends State<MastersPage> {
  final _searchController = TextEditingController();
  String _selectedMasterType = 'Все';
  List<Master> _allMasters = [];
  List<Master> _filteredMasters = [];
  List<Service> _allServices = [];

  @override
  void initState() {
    super.initState();
    _allMasters = DataService.getMasters();
    _allServices = DataService.getServices();
    _filteredMasters = _allMasters;
    _searchController.addListener(_filterMasters);
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _filterMasters() {
    setState(() {
      final searchQuery = _searchController.text.toLowerCase();
      final masterType = _selectedMasterType;

      _filteredMasters = _allMasters.where((master) {
        // Search filter
        if (searchQuery.isNotEmpty &&
            !master.name.toLowerCase().contains(searchQuery)) {
          return false;
        }

        // Master type filter
        if (masterType != 'Все' && master.type != masterType.toLowerCase()) {
          return false;
        }

        return true;
      }).toList();
    });
  }

  int _getServiceCount(String masterId) {
    return _allServices.where((s) => s.masterId == masterId).length;
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
                'Мастеры',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 24),
              // Search
              CustomInput(
                hint: 'Поиск мастера...',
                controller: _searchController,
                prefixIcon: Icon(Icons.search, color: AppColors.mutedForeground, size: 20),
              ),
              const SizedBox(height: 16),
              // Filter
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
                  _filterMasters();
                },
              ),
              const SizedBox(height: 24),
              // Masters list
              if (_filteredMasters.isEmpty)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 32),
                  child: Center(
                    child: Text(
                      'Мастера не найдены',
                      style: TextStyle(
                        color: AppColors.mutedForeground,
                        fontSize: 16,
                      ),
                    ),
                  ),
                )
              else
                ..._filteredMasters.map((master) {
                  final serviceCount = _getServiceCount(master.id);
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: CustomCard(
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => MasterServicesPage(masterId: master.id),
                          ),
                        );
                      },
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      master.name,
                                      style: const TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      Formatters.capitalize(master.type),
                                      style: TextStyle(
                                        fontSize: 14,
                                        color: AppColors.primary,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Text(
                                '$serviceCount услуг',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: AppColors.mutedForeground,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Row(
                            children: [
                              Icon(Icons.phone, size: 14, color: AppColors.mutedForeground),
                              const SizedBox(width: 8),
                              Text(
                                master.phone,
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

