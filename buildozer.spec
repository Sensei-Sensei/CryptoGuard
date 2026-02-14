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

# (str) Application version
version = 1.0

# (list) Application requirements
# pyjnius é essencial para o botão "Enviar/Compartilhar" funcionar no Android
requirements = python3,kivy,pyjnius

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android architecture to build for
android.archs = arm64-v8a

# (str) Icon of the application (descomente e aponte para um arquivo se tiver um ícone)
#icon.filename = %(source.dir)s/icon.png

# (str) Presplash screen of the application
#presplash.filename = %(source.dir)s/presplash.png

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

[android]
# (bool) Use the custom screen for the splash screen
android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java classes to add to the compilation
# Isso ajuda a garantir que o Pyjnius encontre as classes nativas do Android
android.add_jars =
