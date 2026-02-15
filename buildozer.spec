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

# (str) Versão do aplicativo (Aumente sempre que atualizar o APK)
version = 1.7

# (list) Requisitos da aplicação
# ADICIONADO: sdl2_ttf e sdl2_image para renderizar ícones e fontes corretamente
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pyjnius, pillow, setuptools, hostpython3, sdl2_ttf, sdl2_image

# (str) Orientação suportada (retrato)
orientation = portrait

# (bool) Indicar se a aplicação deve ser tela cheia ou não
fullscreen = 0

# (list) Permissões do Android
android.permissions = INTERNET

# (int) Target Android API (33 atende aos requisitos atuais da Google Play)
android.api = 33

# (int) API mínima suportada
android.minapi = 21

# (int) Versão do SDK do Android
android.sdk = 33

# (str) Versão do NDK do Android
android.ndk = 25b

# (bool) Aceitar automaticamente as licenças do SDK
android.accept_sdk_license = True

# (str) Arquitetura para build
android.archs = arm64-v8a

[buildozer]
# (int) Nível de log (2 para ver erros detalhados se falhar)
log_level = 2

# (int) Exibir aviso se rodar como root
warn_on_root = 1

[android]
# (str) Nome da atividade principal
android.entrypoint = org.kivy.android.PythonActivity

# (str) Modo de entrada suave (ESSENCIAL para o corretor ortográfico e redimensionamento do teclado)
android.window_softinput_mode = adjustResize

# (str) Atributos extras do manifesto para garantir sugestões de teclado
android.manifest.attributes = android:windowSoftInputMode="stateUnspecified|adjustResize"

# (list) Classes Java para compilação (Pyjnius)
android.add_jars =
