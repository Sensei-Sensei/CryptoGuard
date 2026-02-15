[app]
# (str) Title of your application
title = CryptoGuard

# (str) Package name
package.name = cryptoguard

# (str) Package domain (needed for android packaging)
package.domain = com.stazin

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 3.2

# (list) Application requirements
# ADICIONADO: openssl e sqlite3 para evitar crash no hashlib
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, pillow, setuptools, hostpython3, sdl2_ttf, sdl2_image, openssl, sqlite3

# (str) Custom source folders for requirements
# Comentado para usar as versões estáveis do p4a
# requirements.source.kivymd = ../kivymd

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support.
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
# android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded)
# android.sdk_path = 

# (str) ANT directory (if empty, it will be automatically downloaded)
# android.ant_path = 

# (bool) If True, then skip trying to update the Android sdk
# Ativado para usar o que preparamos no workflow do GitHub
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only.
android.accept_sdk_license = True

# (str) Android entry point, default is to use start.py
android.entrypoint = org.kivy.android.PythonActivity

# (list) Pattern to whitelist for the whole project
# android.whitelist = 

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# arm64-v8a é o padrão para Play Store e celulares modernos
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (list) Gradle dependencies
android.gradle_dependencies = 'com.google.android.material:material:1.9.0'

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifacts (optional, default is <app dir>/.buildozer)
# build_dir = ./.buildozer

# (str) Path to bin directory (optional, default is <app dir>/bin)
# bin_dir = ./bin
