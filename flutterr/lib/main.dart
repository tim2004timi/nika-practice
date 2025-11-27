import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'theme/app_theme.dart';
import 'pages/login_page.dart';
import 'pages/register_page.dart';
import 'pages/home_page.dart';
import 'pages/services_page.dart';
import 'pages/service_detail_page.dart';
import 'pages/masters_page.dart';
import 'pages/master_services_page.dart';
import 'widgets/bottom_nav.dart';
import 'services/storage_service.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Николь Бьюти',
      theme: AppTheme.darkTheme,
      debugShowCheckedModeBanner: false,
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginPage(),
        '/register': (context) => const RegisterPage(),
        '/': (context) => const MainWrapper(),
        '/services': (context) => const MainWrapper(initialIndex: 1),
        '/masters': (context) => const MainWrapper(initialIndex: 2),
        '/service': (context) {
          final args = ModalRoute.of(context)!.settings.arguments as Map<String, String>;
          return ServiceDetailPage(serviceId: args['id']!);
        },
        '/master': (context) {
          final args = ModalRoute.of(context)!.settings.arguments as Map<String, String>;
          return MasterServicesPage(masterId: args['id']!);
        },
      },
      onGenerateRoute: (settings) {
        if (settings.name == null) return null;

        // Handle /service/:id
        if (settings.name!.startsWith('/service/')) {
          final id = settings.name!.split('/service/')[1];
          return MaterialPageRoute(
            builder: (context) => ServiceDetailPage(serviceId: id),
          );
        }

        // Handle /master/:id
        if (settings.name!.startsWith('/master/')) {
          final id = settings.name!.split('/master/')[1];
          return MaterialPageRoute(
            builder: (context) => MasterServicesPage(masterId: id),
          );
        }

        return null;
      },
    );
  }
}

class MainWrapper extends StatefulWidget {
  final int initialIndex;

  const MainWrapper({super.key, this.initialIndex = 0});

  @override
  State<MainWrapper> createState() => _MainWrapperState();
}

class _MainWrapperState extends State<MainWrapper> {
  int _currentIndex = 0;
  bool _isAuthenticated = false;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialIndex;
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    final isAuth = await StorageService.isAuthenticated();
    setState(() {
      _isAuthenticated = isAuth;
      _isLoading = false;
    });

    if (!_isAuthenticated && mounted) {
      Navigator.of(context).pushReplacementNamed('/login');
    }
  }

  void _onTabTapped(int index) {
    setState(() {
      _currentIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (!_isAuthenticated) {
      return const SizedBox.shrink();
    }

    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: const [
          HomePage(),
          ServicesPage(),
          MastersPage(),
        ],
      ),
      bottomNavigationBar: BottomNav(
        currentIndex: _currentIndex,
        onTap: _onTabTapped,
      ),
    );
  }
}
