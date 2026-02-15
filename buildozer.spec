[app]
title = CryptoGuard
package.name = cryptoguard
package.domain = com.stazin
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.8

# REQUISITOS CORRIGIDOS: Adicionado sqlite3 e openssl que o hashlib usa
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, pillow, setuptools, hostpython3, sdl2_ttf, sdl2_image, openssl, sqlite3

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# APIs E NDK (Compatibilidade Máxima)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Garante que o Gradle use a versão correta
android.gradle_dependencies = 'com.google.android.material:material:1.9.0'

[buildozer]
log_level = 2
warn_on_root = 1
