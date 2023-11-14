import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Class that overrides the default [HttpClient] to allow self signed
class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    // Allow self signed certificate
    return super.createHttpClient(context)
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
  }
}

// Create a global ProviderContainer, that will be used through the app
final container = ProviderContainer();

/// Main application widget.
/// This is the root widget of your application.
/// Use this class to instantiate your app, and to set the main theme.
/// This class is also responsible for setting the main routes of your app.
/// You can also use this class to set the main providers of your app.
void main() async {
  // Ensure that all the widgets are loaded before running the app
  WidgetsFlutterBinding.ensureInitialized();

  // Check if the app is running in debug mode
  if (kDebugMode) {
    // Authorise self signed certificate in debug mode
    HttpOverrides.global = MyHttpOverrides();
  }

  // Run the app
  runApp(
    // Wrap the app in a ProviderScope to allow the use of providers
    UncontrolledProviderScope(
      // Pass the container to the ProviderScope
      container: container,
      // Define the main widget of the app
      child: const Application(),
    ),
  );
}
