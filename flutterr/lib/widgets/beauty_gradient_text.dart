import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

class BeautyGradientText extends StatelessWidget {
  final String text;
  final double fontSize;
  final FontWeight fontWeight;

  const BeautyGradientText({
    super.key,
    required this.text,
    this.fontSize = 36,
    this.fontWeight = FontWeight.bold,
  });

  @override
  Widget build(BuildContext context) {
    return ShaderMask(
      shaderCallback: (bounds) => const LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          AppColors.primary, // hsl(35, 45%, 70%)
          AppColors.caramel, // hsl(32, 40%, 50%)
        ],
      ).createShader(bounds),
      child: Text(
        text,
        style: TextStyle(
          fontSize: fontSize,
          fontWeight: fontWeight,
          color: Colors.white,
        ),
      ),
    );
  }
}

