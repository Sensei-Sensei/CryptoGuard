[app]
title = CryptoGuard
package.name = cryptoguard
package.domain = com.stazin
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.1

requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, pillow, setuptools, hostpython3, sdl2_ttf, sdl2_image, openssl, sqlite3

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Configurações de API
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

# Essencial para automação
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
