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

# (str) Application versioning - Versão 3.4 para resetar caches
version = 3.4

# (list) Application requirements
# ORDEM CRÍTICA: hostpython3 e setuptools primeiro ajudam na compilação do C
requirements = python3, hostpython3, kivy==2.3.0, kivymd==1.2.0, pillow, openssl, sqlite3, pyjnius, setuptools

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use (25b é a única 100% estável hoje)
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) Pular atualização automática para não conflitar com o GitHub
android.skip_update = False

# (bool) Aceitar licenças automaticamente
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Arquitetura Alvo
# IMPORTANTE: Mantenha APENAS arm64-v8a. Compilar para duas arquiteturas 
# ao mesmo tempo é o que faz o GitHub "matar" o processo por falta de RAM.
android.archs = arm64-v8a

# (bool) Habilitar AndroidX (Necessário para KivyMD)
android.enable_androidx = True

# (list) Dependências Gradle
android.gradle_dependencies = 'com.google.android.material:material:1.9.0'

[buildozer]
# (int) Log level (2 para debug detalhado)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
