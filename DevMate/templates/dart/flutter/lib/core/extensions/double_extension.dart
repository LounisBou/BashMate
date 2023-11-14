extension DoubleExtension on double {
  String get toEuro {
    return '${toStringAsFixed(2)} €'.replaceAll('.', ',');
  }

  String get toDollar {
    return '${toStringAsFixed(2)} \$'.replaceAll('.', ',');
  }

  String get toPercent {
    return '${toStringAsFixed(2)} %'.replaceAll('.', ',');
  }

  String get toKm {
    if (this > 10) {
      return '${toStringAsFixed(0)} km';
    }
    if (this >= 1) {
      return '${toStringAsFixed(2)} km';
    }
    return '${toStringAsFixed(3)} km';
  }
}
