import 'package:flutter/material.dart';
import '../widgets/custom_card.dart';
import '../widgets/custom_input.dart';
import '../services/api_service.dart';
import '../theme/app_colors.dart';
import '../models/master.dart';
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
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadMasters();
    _searchController.addListener(_filterMasters);
  }

  Future<void> _loadMasters() async {
    setState(() {
      _isLoading = true;
    });
    try {
      final masters = await ApiService.getMasters();
      setState(() {
        _allMasters = masters;
        _filteredMasters = masters;
        _isLoading = false;
      });
      _filterMasters();
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ошибка загрузки мастеров: ${e.toString()}'),
            backgroundColor: AppColors.destructive,
          ),
        );
      }
    }
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
        if (masterType != 'Все') {
          final masterRole = master.role.toUpperCase();
          final filterRole = masterType.toUpperCase();
          // Map Russian names to API roles
          final roleMap = {
            'ВИЗАЖИСТ': 'VIZAZHIST',
            'МАНИКЮРИСТ': 'MANICURIST',
            'СТИЛИСТ': 'STYLIST',
            'БРОВИСТ': 'BROWIST',
          };
          final apiRole = roleMap[filterRole];
          if (apiRole != null && masterRole != apiRole) {
            return false;
          } else if (apiRole == null && masterRole != filterRole) {
            return false;
          }
        }

        return true;
      }).toList();
    });
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _loadMasters,
          color: AppColors.primary,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
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
              if (_isLoading)
                const Center(
                  child: Padding(
                    padding: EdgeInsets.all(32.0),
                    child: CircularProgressIndicator(),
                  ),
                )
              else if (_filteredMasters.isEmpty)
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
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: CustomCard(
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => MasterServicesPage(masterId: master.id.toString()),
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
                                      Formatters.formatRole(master.role),
                                      style: TextStyle(
                                        fontSize: 14,
                                        color: AppColors.primary,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Text(
                                '${master.servicesCount} услуг',
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
      ),
    );
  }
}

