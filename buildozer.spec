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

# (str) Application versioning (Agregue sempre para evitar conflito de cache)
version = 4.1

# (list) Application requirements
# ADICIONADO: openssl e sqlite3 (essenciais para hashlib e persistência)
# ADICIONADO: hostpython3 e setuptools (ajudam na estabilidade do build)
requirements = python3,hostpython3,kivy==2.3.0,kivymd==1.2.0,pillow,openssl,sqlite3,pyjnius

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

# (str) Android NDK version to use (25b é a recomendada para Kivy 2.3.0)
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) Aceitar licenças automaticamente
android.accept_sdk_license = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (list) Android architectures to build for
# ATUALIZADO: Incluído armeabi-v7a caso seu celular seja 32 bits
android.archs = arm64-v8a, armeabi-v7a

# (bool) Habilitar AndroidX (Necessário para KivyMD)
android.enable_androidx = True

# (list) Dependências Gradle
# CORRIGIDO: Sem aspas para evitar erro de sintaxe no build.gradle
android.gradle_dependencies = com.google.android.material:material:1.5.0

# (bool) Copy libraries to the libs directory (ajuda no carregamento de .so)
android.copy_libs = 1

[buildozer]
# (int) Log level (2 para debug detalhado)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
