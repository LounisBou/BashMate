class Config {
  factory Config() => _instance;

  Config._internal() {
    //data = kDebugMode ? configPreprod : configProd;
    data = configPreprod;
  }

  static final Config _instance = Config._internal();

  late final ConfigDto data;
}

class ConfigDto {
  const ConfigDto({
    required this.apiDomain,
    required this.apiVersion,
  });

  final String apiDomain;
  final String apiVersion;

  String get apiUrl => '$apiDomain/$apiVersion';
}

const configLocal = ConfigDto(
  apiDomain: 'https://api.example.local',
  apiVersion: 'v1',
);

const configPreprod = ConfigDto(
  apiDomain: 'https://preprod-api.example.com',
  apiVersion: 'v1',
);

const configProd = ConfigDto(
  apiDomain: 'https://api.example.com',
  apiVersion: 'v1',
);
