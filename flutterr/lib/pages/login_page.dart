import 'package:flutter/material.dart';
import '../widgets/beauty_gradient_text.dart';
import '../widgets/custom_input.dart';
import '../widgets/custom_button.dart';
import '../services/storage_service.dart';
import '../services/api_service.dart';
import '../theme/app_colors.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _loginController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _loginController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (_formKey.currentState!.validate()) {
      try {
        final response = await ApiService.login(
          username: _loginController.text,
          password: _passwordController.text,
        );
        
        await StorageService.setToken(response.accessToken);
        await StorageService.setUserId(response.user.id);
        await StorageService.setUserName(response.user.fullName);
        
        if (mounted) {
          Navigator.of(context).pushReplacementNamed('/');
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Ошибка входа: ${e.toString()}'),
              backgroundColor: AppColors.destructive,
            ),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 384),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const BeautyGradientText(text: 'Николь Бьюти'),
                  const SizedBox(height: 8),
                  Text(
                    'Добро пожаловать',
                    style: TextStyle(
                      fontSize: 18,
                      color: AppColors.mutedForeground,
                    ),
                  ),
                  const SizedBox(height: 48),
                  CustomInput(
                    label: 'Логин',
                    controller: _loginController,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Введите логин';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 24),
                  CustomInput(
                    label: 'Пароль',
                    controller: _passwordController,
                    obscureText: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Введите пароль';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 24),
                  CustomButton(
                    text: 'Войти',
                    onPressed: _handleLogin,
                    isFullWidth: true,
                  ),
                  const SizedBox(height: 16),
                  Center(
                    child: TextButton(
                      onPressed: () {
                        Navigator.of(context).pushNamed('/register');
                      },
                      child: Text(
                        'Регистрация',
                        style: TextStyle(
                          fontSize: 14,
                          color: AppColors.primary,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

