[app]
title = CryptoGuard
package.name = cryptoguard
package.domain = com.stazin
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.1

# REQUISITOS (O Pillow é necessário para os ícones do KivyMD)
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, pillow, setuptools

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.entrypoint = org.kivy.android.PythonActivity
# Permite que o teclado interaja melhor com o layout
android.window_softinput_mode = adjustResize
