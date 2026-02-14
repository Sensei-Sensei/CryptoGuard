[app]
# (str) Título do seu aplicativo
title = CryptoGuard

# (str) Nome do pacote (sem espaços ou acentos)
package.name = cryptoguard

# (str) Domínio do pacote
package.domain = com.stazin

# (str) Diretório onde o main.py está localizado
source.dir = .

# (list) Extensões de arquivos a serem incluídas
source.include_exts = py,png,jpg,kv,atlas

# (str) Versão do aplicativo
version = 1.0

# (list) Requisitos da aplicação
# ADICIONADO: pyjnius (essencial para o botão ENVIAR no Android)
requirements = python3,kivy,pyjnius

# (str) Orientação suportada (retrato)
orientation = portrait

# (bool) Indicar se a aplicação deve ser tela cheia ou não
fullscreen = 0

# (list) Permissões do Android
android.permissions = INTERNET

# (int) Target Android API (33 é o padrão atual do Google Play)
android.api = 33

# (int) API mínima suportada
android.minapi = 21

# (int) Versão do SDK do Android
android.sdk = 33

# (str) Versão do NDK do Android
android.ndk = 25b

# (bool) Aceitar automaticamente as licenças do SDK
android.accept_sdk_license = True

# (str) Arquitetura para build (arm64-v8a atende 99% dos celulares novos)
android.archs = arm64-v8a

[buildozer]
# (int) Nível de log (2 para ver erros detalhados se falhar)
log_level = 2

# (int) Exibir aviso se rodar como root
warn_on_root = 1

[android]
# (str) Nome da atividade principal
android.entrypoint = org.kivy.android.PythonActivity

# (list) Classes Java para compilação (necessário para Pyjnius)
android.add_jars =
