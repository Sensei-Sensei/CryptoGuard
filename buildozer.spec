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

# (str) Application version (Aumentado para garantir nova instalação)
version = 2.0

# (list) Application requirements
# Adicionado sdl2_image e sdl2_ttf explicitamente
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, pillow, setuptools, hostpython3, sdl2_ttf, sdl2_image

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess download.
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only.
android.accept_sdk_license = True

# (str) Android architecture to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1

[android]
# (str) The Android arch to build for
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra window attributes
android.window_softinput_mode = adjustResize
android.manifest.attributes = android:windowSoftInputMode="stateUnspecified|adjustResize"
