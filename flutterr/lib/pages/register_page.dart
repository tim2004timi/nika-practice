import 'package:flutter/material.dart';
import '../widgets/beauty_gradient_text.dart';
import '../widgets/custom_input.dart';
import '../widgets/custom_button.dart';
import '../services/storage_service.dart';
import '../services/api_service.dart';
import '../theme/app_colors.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _loginController = TextEditingController();
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController(text: '+7');
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    _loginController.dispose();
    _nameController.dispose();
    _phoneController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _handleRegister() async {
    if (_formKey.currentState!.validate()) {
      try {
        final response = await ApiService.register(
          login: _loginController.text,
          password: _passwordController.text,
          fullName: _nameController.text,
          phoneNumber: _phoneController.text,
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
              content: Text('Ошибка регистрации: ${e.toString()}'),
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
                    'Регистрация',
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
                  const SizedBox(height: 16),
                  CustomInput(
                    label: 'ФИО',
                    controller: _nameController,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Введите ФИО';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
                  CustomInput(
                    label: 'Телефон',
                    controller: _phoneController,
                    keyboardType: TextInputType.phone,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Введите телефон';
                      }
                      if (!value.startsWith('+7')) {
                        return 'Телефон должен начинаться с +7';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),
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
                  const SizedBox(height: 16),
                  CustomInput(
                    label: 'Повторите пароль',
                    controller: _confirmPasswordController,
                    obscureText: true,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Повторите пароль';
                      }
                      if (value != _passwordController.text) {
                        return 'Пароли не совпадают';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 24),
                  CustomButton(
                    text: 'Зарегистрироваться',
                    onPressed: _handleRegister,
                    isFullWidth: true,
                  ),
                  const SizedBox(height: 16),
                  Center(
                    child: TextButton(
                      onPressed: () {
                        Navigator.of(context).pushReplacementNamed('/login');
                      },
                      child: Text(
                        'Войти',
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

