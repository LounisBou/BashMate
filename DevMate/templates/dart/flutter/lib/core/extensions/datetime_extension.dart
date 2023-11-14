/// Extension on DateTime
extension DateTimeExtension on DateTime {
  bool get isPublicHoliday {
    DateTime easterDate = getEaster(year);

    List<DateTime> holidays = [
      DateTime(year, 1, 1), // 1er janvier
      DateTime(year, 5, 1), // Fête du travail
      DateTime(year, 5, 8), // Victoire des alliés
      DateTime(year, 7, 14), // Fête nationale
      DateTime(year, 8, 15), // Assomption
      DateTime(year, 11, 1), // Toussaint
      DateTime(year, 11, 11), // Armistice
      DateTime(year, 12, 25), // Noël

      // Dates variables basées sur Pâques
      DateTime(easterDate.year, easterDate.month, easterDate.day + 1),
      DateTime(easterDate.year, easterDate.month, easterDate.day + 39),
      DateTime(easterDate.year, easterDate.month, easterDate.day + 50),
    ];

    for (final holiday in holidays) {
      if (year == holiday.year &&
          month == holiday.month &&
          day == holiday.day) {
        return true;
      }
    }

    return false;
  }
}

/// Get easter date for a given year
/// Credit:  https://github.com/nikolajskov/easter/blob/master/lib/easter.dart
DateTime getEaster(int year) {
  if (year < 1583) {
    throw ArgumentError.value(
      year,
      'year',
      'Year cannot be earlier than 1583.',
    );
  } else if (year > 4099) {
    throw ArgumentError.value(year, 'year', 'Year cannot be later than 4099.');
  }

  final g = year % 19;
  final c = year ~/ 100;
  final h = (c - (c ~/ 4) - ((8 * c + 13) ~/ 25) + 19 * g + 15) % 30;
  final i =
      h - (h ~/ 28) * (1 - (h ~/ 28) * (29 ~/ (h + 1)) * ((21 - g) ~/ 11));
  var day = i - ((year + (year ~/ 4) + i + 2 - c + (c ~/ 4)) % 7) + 28;
  var month = 3;

  if (day > 31) {
    month++;
    day -= 31;
  }

  var easter = DateTime(year, month, day);
  return easter;
}
