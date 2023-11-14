# Makefile for Flutter project
# Run `make help` to list available commands.
run :
	fvm flutter packages pub run build_runner build --delete-conflicting-outputs

watch :
	fvm flutter packages pub run build_runner watch --delete-conflicting-outputs

lint :
	dart analyze .

lint-fix :
	dart fix --apply

build :
	fvm flutter build appbundle
	fvm flutter build ipa

refresh-ios :
	fvm flutter clean
	fvm flutter pub get
	fvm flutter packages pub run build_runner build --delete-conflicting-outputs
	cd ios && pod install && cd ..

build-ios :
	fvm flutter clean
	fvm flutter pub get
	fvm flutter packages pub run build_runner build --delete-conflicting-outputs
	cd ios && pod install && cd ..
	fvm flutter build ios

push-ios :
	xcrun altool --validate-app -f file -t ios -u lounis@akawam.com
	xcrun altool --upload-app -f file -t ios -u lounis@akawam.com

build-android :
	fvm flutter clean
	fvm flutter pub get
	fvm flutter packages pub run build_runner build --delete-conflicting-outputs
	fvm flutter build appbundle
	open build/app/outputs/bundle/release/

generate-icons :
	make generate-icons-android
	make generate-icons-ios

generate-icons-android :
	sips --resampleWidth 192 "assets/icon-app.png" --out "android/app/src/main/res/mipmap-xxxhdpi/launcher_icon.png"
	sips --resampleWidth 512 "assets/icon-app.png" --out "android/app/src/main/res/mipmap-xxhdpi/launcher_icon.png"
	sips --resampleWidth 96 "assets/icon-app.png" --out "android/app/src/main/res/mipmap-xhdpi/launcher_icon.png"
	sips --resampleWidth 72 "assets/icon-app.png" --out "android/app/src/main/res/mipmap-hdpi/launcher_icon.png"
	sips --resampleWidth 48 "assets/icon-app.png" --out "android/app/src/main/res/mipmap-mdpi/launcher_icon.png"

generate-icons-ios :
	sips --resampleWidth 16 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/16.png"
	sips --resampleWidth 20 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/20.png"
	sips --resampleWidth 29 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/29.png"
	sips --resampleWidth 32 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/32.png"
	sips --resampleWidth 40 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/40.png"
	sips --resampleWidth 48 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/48.png"
	sips --resampleWidth 50 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/50.png"
	sips --resampleWidth 55 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/55.png"
	sips --resampleWidth 57 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/57.png"
	sips --resampleWidth 58 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/58.png"
	sips --resampleWidth 60 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/60.png"
	sips --resampleWidth 64 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/64.png"
	sips --resampleWidth 66 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/66.png"
	sips --resampleWidth 72 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/72.png"
	sips --resampleWidth 76 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/76.png"
	sips --resampleWidth 80 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/80.png"
	sips --resampleWidth 87 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/87.png"
	sips --resampleWidth 88 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/88.png"
	sips --resampleWidth 92 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/92.png"
	sips --resampleWidth 100 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/100.png"
	sips --resampleWidth 102 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/102.png"
	sips --resampleWidth 114 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/114.png"
	sips --resampleWidth 120 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/120.png"
	sips --resampleWidth 128 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/128.png"
	sips --resampleWidth 144 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/144.png"
	sips --resampleWidth 152 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/152.png"
	sips --resampleWidth 167 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/167.png"
	sips --resampleWidth 172 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/172.png"
	sips --resampleWidth 180 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/180.png"
	sips --resampleWidth 196 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/196.png"
	sips --resampleWidth 216 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/216.png"
	sips --resampleWidth 256 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/256.png"
	sips --resampleWidth 512 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/512.png"
	sips --resampleWidth 1024 "assets/icon-app.png" --out "ios/Runner/Assets.xcassets/AppIcon.appiconset/1024.png"