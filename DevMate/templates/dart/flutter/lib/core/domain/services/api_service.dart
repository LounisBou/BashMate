import 'dart:async';
import 'dart:io' show Platform;
import 'package:dio/dio.dart';
import 'package:[APP_PACKAGE_NAME]/config.dart';
import 'package:[APP_PACKAGE_NAME]/main.dart';

class ApiService {
  ApiService();

  static Dio? dio;
  static String? _applicationVersion;
  static final _controller = StreamController<String?>.broadcast();

  static Stream<String?> get stream => _controller.stream.asBroadcastStream();
  static Map<String, dynamic> defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'device': 'mobile',
    'os': Platform.operatingSystem,
    'os-version': Platform.operatingSystemVersion,
    'device-locale': Platform.localeName,
    'device-locale-country': Platform.localeName,
  };

  /// Reset Dio instance
  static void resetInstance() {
    dio = Dio();

    dio?.interceptors.add(
      InterceptorsWrapper(
        onError: (DioException e, ErrorInterceptorHandler handler) {
          handler.resolve(
            Response(
              requestOptions: e.requestOptions,
              statusCode: 500, // Code pour timeout
              data: {
                'type': 'error',
                'message': 'Une erreur est survenue',
                'validationErrors': null,
                'data': null,
              },
            ),
          );
        },
        onRequest: (options, handler) async {
          // Add default headers to all requests
          options.headers.addAll(defaultHeaders);
          options.headers['X-Api-Version'] =
              await ApiService.applicationVersion;
          options.validateStatus = (status) => true;
          return handler.next(options); //continue
        },
        onResponse: (response, handler) {
          if (response.statusCode == 401) {
            resetToken();
          }
          return handler.next(response);
        },
      ),
    );

    dio?.options.baseUrl = Config().data.apiUrl;
    dio?.options.connectTimeout = const Duration(seconds: 10);
  }

  /// Get a new Dio instance
  static Dio getDioInstance() {
    if (dio == null) {
      resetInstance();
    }
    return dio!;
  }

  // Add interceptor on Dio instance
  static void addInterceptor(Dio instance) {
    instance.interceptors.add(
      InterceptorsWrapper(
        onError: (DioException e, ErrorInterceptorHandler handler) {
          handler.resolve(
            Response(
              requestOptions: e.requestOptions,
              statusCode: 500, // Code pour timeout
              data: {
                'type': 'error',
                'message': 'Une erreur est survenue',
                'validationErrors': null,
                'data': null,
              },
            ),
          );
        },
        onResponse: (response, handler) {
          response.data ??= {
            'type': 'error',
            'message': 'Une erreur est survenue',
            'validationErrors': null,
            'data': null,
          };
          return handler.next(response);
        },
        onRequest: (options, handler) async {
          // Add default headers to all requests
          options.headers.addAll(defaultHeaders);
          options.headers['X-Api-Version'] =
              await ApiService.applicationVersion;
          options.validateStatus = (status) => true;
          return handler.next(options);
        },
      ),
    );
  }

  /// Get the application version from the package info
  static Future<String> get applicationVersion async {
    if (_applicationVersion == null) {
      final PackageInfo packageInfo = await PackageInfo.fromPlatform();
      _applicationVersion = packageInfo.version;
    }
    return _applicationVersion!;
  }
}
