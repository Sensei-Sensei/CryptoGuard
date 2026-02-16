[app]
title = CryptoGuard
package.name = cryptoguard
package.domain = com.cryptoguard
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 4.2

# Requirements: Essencial incluir libffi para compatibilidade de sistema
requirements = python3,hostpython3,kivy==2.3.0,kivymd==1.2.0,pillow,openssl,sqlite3,pyjnius,libffi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = True
android.entrypoint = org.kivy.android.PythonActivity

# Build para ambas as arquiteturas para garantir que funcione no seu celular
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
android.gradle_dependencies = com.google.android.material:material:1.5.0
android.copy_libs = 1

[buildozer]
log_level = 2
warn_on_root = 1
