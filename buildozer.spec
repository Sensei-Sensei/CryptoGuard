[app]
title = CryptoGuard
package.name = cryptoguard
package.domain = com.stazin
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.9

# Requirements - Removi espaços extras
requirements = python3,hostpython3,kivy==2.3.0,kivymd==1.2.0,pillow,openssl,sqlite3,pyjnius

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.skip_update = False
android.accept_sdk_license = True
android.entrypoint = org.kivy.android.PythonActivity
android.archs = arm64-v8a
android.enable_androidx = True

# CORREÇÃO AQUI: Sem aspas simples extras, apenas a lista separada por vírgula
android.gradle_dependencies = com.google.android.material:material:1.5.0

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = ./bin
