import 'dart:math';

extension ListExtension on List {
  T random<T>() {
    final random = Random();
    final i = random.nextInt(length);
    return this[i];
  }
}
