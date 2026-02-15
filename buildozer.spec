[app]

# (str) Nome do aplicativo
title = CryptoGuard

# (str) Nome do pacote
package.name = cryptoguard

# (str) Domínio do pacote
package.domain = com.stazin

# (str) Diretório onde está o main.py
source.dir = .

# (list) Extensões de arquivos a serem incluídos
source.include_exts = py,png,jpg,kv,atlas

# (str) Versão do App - Suba para 3.3 para limpar caches antigos
version = 3.3

# (list) Requisitos do Aplicativo
# A ordem aqui é vital. hostpython3 e setuptools garantem a compilação.
# openssl e sqlite3 são obrigatórios para as funções de hashlib e seguranca.
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, openssl, sqlite3, pyjnius, setuptools, hostpython3

# (str) Orientação da tela
orientation = portrait

# (bool) Fullscreen (0 para mostrar a barra de status, melhor para apps de ferramentas)
fullscreen = 0

# (list) Permissões do Android
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) API alvo (33 é o padrão atual da Play Store)
android.api = 33

# (int) API mínima suportada
android.minapi = 21

# (int) Versão do SDK do Android a usar
android.sdk = 33

# (str) Versão do NDK do Android (25b é a mais estável para Kivy/KivyMD)
android.ndk = 25b

# (int) API do NDK do Android
android.ndk_api = 21

# (bool) Usar armazenamento privado (Recomendado: True)
android.private_storage = True

# (bool) Pular atualização do SDK (Deixe False para o GitHub preparar o ambiente)
android.skip_update = False

# (bool) Aceitar licenças automaticamente
android.accept_sdk_license = True

# (str) Ponto de entrada do Android
android.entrypoint = org.kivy.android.PythonActivity

# (str) Arquitetura alvo
# Usamos apenas arm64-v8a para o build ser mais rápido e economizar RAM no GitHub.
# Celulares modernos (99%) usam arm64.
android.archs = arm64-v8a

# (bool) Habilitar backup automático
android.allow_backup = True

# (list) Dependências Gradle (Necessário para alguns componentes do KivyMD)
android.gradle_dependencies = 'com.google.android.material:material:1.9.0'

# (bool) Ativar suporte a Android X (Obrigatório para KivyMD moderno)
android.enable_androidx = True

[buildozer]

# (int) Nível de Log (2 para debug detalhado caso algo falhe)
log_level = 2

# (int) Exibir aviso se rodar como root
warn_on_root = 1

# (str) Caminho para os artefatos de build (opcional)
# build_dir = ./.buildozer

# (str) Caminho para o diretório de saída (onde o APK aparecerá)
bin_dir = ./bin
