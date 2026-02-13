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

# (list) Application requirements
# ADICIONE OUTRAS LIBs AQUI, ex: python3,kivy,requests
requirements = python3,kivy

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

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess bandwidth usage or fail on some platforms.
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# THIS IS CRITICAL FOR GITHUB ACTIONS
android.accept_sdk_license = True

# (str) Android architecture to build for
android.archs = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
