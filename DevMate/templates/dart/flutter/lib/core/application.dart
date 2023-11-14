import 'package:flutter/material.dart';
import 'package:[APP_PACKAGE_NAME]/core/presentation/router/app_router_delegate.dart';

class Application extends StatelessWidget {
  const Application({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      theme: ThemeData(
        useMaterial3: false,
        primaryColor: Colors.black,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.red),
      ),
      debugShowCheckedModeBanner: false,
      locale: const Locale('fr'),
      routerDelegate: AppRouterDelegate(),
    );
  }
}
