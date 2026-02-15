import hashlib
import base64
import secrets
import threading
from kivy.config import Config

# 1. Configurações de teclado e janela ANTES de importar o resto do Kivy
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('graphics', 'resizable', '0')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import mainthread
from kivy.core.window import Window

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal com respiro para a barra de notificações
        layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(40), dp(20), dp(20)], spacing=dp(15))
        
        # Header - Título do App
        layout.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H5",
            bold=True, theme_text_color="Custom", text_color=(0, 0.8, 1, 1),
            size_hint_y=None, height=dp(50)
        ))

        # Card Central de Operações
        self.card = MDCard(
            orientation='vertical', padding=dp(15), spacing=dp(15),
            elevation=0, radius=[20,], md_bg_color=(1, 1, 1, 0.05),
            size_hint_y=None, height=dp(420), line_color=(1, 1, 1, 0.1)
        )

        # Campos de entrada
        self.msg_input = MDTextField(
            hint_text="Mensagem ou Código", mode="rectangle", 
            multiline=True, keyboard_suggestions=False
        )
        self.pwd_input = MDTextField(
            hint_text="Chave de Acesso", password=True, 
            mode="rectangle", keyboard_suggestions=False
        )
        
        self.card.add_widget(self.msg_input)
        self.card.add_widget(self.pwd_input)

        # Botões de Proteção e Revelação
        btns = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        btns.add_widget(MDFillRoundFlatIconButton(
            icon="shield-lock", text="PROTEGER", 
            on_release=self.start_encrypt, size_hint_x=0.5
        ))
        btns.add_widget(MDFillRoundFlatIconButton(
            icon="lock-open", text="REVELAR", 
            on_release=self.start_decrypt, size_hint_x=0.5
        ))
        
        self.card.add_widget(btns)

        # Feedback visual de status
        self.res_label = MDLabel(
            text="Pronto para uso", halign="center", 
            theme_text_color="Secondary", font_style="Caption"
        )
        self.card.add_widget(self.res_label)

        layout.add_widget(self.card)
        layout.add_widget(MDBoxLayout()) # Espaçador
        self.add_widget(layout)

    def show_message(self, text, is_error=False):
        color = (0.8, 0.2, 0.2, 1) if is_error else (0, 0.6, 0.4, 1)
        Snackbar(text=text, bg_color=color, duration=2).open()

    @mainthread
    def update_ui(self, result, info_text, is_error=False):
        """Atualiza a interface com segurança a partir de qualquer Thread"""
        self.res_label.text = info_text
        if not is_error and result:
            Clipboard.copy(result)
            if "Criptografado" in info_text:
                self.msg_input.text = "" # Limpa entrada original por segurança
            else:
                self.msg_input.text = result # Coloca texto revelado no campo
        
        self.show_message(info_text, is_error)

    # --- LÓGICA DE CRIPTOGRAFIA EM BACKGROUND ---

    def start_encrypt(self, *args):
        self.res_label.text = "Processando..."
        threading.Thread(target=self._encrypt_task, daemon=True).start()

    def _encrypt_task(self):
        msg = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()
        
        if not msg or not pwd:
            self.update_ui("", "Preencha texto e chave!", True)
            return

        try:
            # PBKDF2 leva tempo, rodar aqui não trava o botão
            salt = secrets.token_bytes(16)
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            nonce = secrets.token_bytes(8)
            data = nonce + msg.encode('utf-8')
            
            # Algoritmo customizado para evitar dependências externas pesadas (como PyCrypto)
            expanded = b''
            for i in range((len(data) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            
            enc = bytes(a ^ b for a, b in zip(data, expanded))
            auth_tag = hashlib.sha256(key + enc).digest()[:16]
            
            final_code = base64.b64encode(salt + auth_tag + enc).decode()
            self.update_ui(final_code, "Criptografado e Copiado!")
        except Exception as e:
            self.update_ui("", f"Erro: {str(e)}", True)

    def start_decrypt(self, *args):
        self.res_label.text = "Verificando..."
        threading.Thread(target=self._decrypt_task, daemon=True).start()

    def _decrypt_task(self):
        code = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()

        if not code or not pwd:
            self.update_ui("", "Falta código ou chave!", True)
            return

        try:
            raw = base64.b64decode(code)
            if len(raw) < 32: raise ValueError("Código curto demais")
            
            salt, auth_tag, enc = raw[:16], raw[16:32], raw[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            
            # Validar integridade
            if hashlib.sha256(key + enc).digest()[:16] != auth_tag:
                self.update_ui("", "Chave de acesso incorreta!", True)
                return

            expanded = b''
            for i in range((len(enc) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            
            result = bytes(a ^ b for a, b in zip(enc, expanded))[8:].decode('utf-8')
            self.update_ui(result, "Mensagem Revelada!")
        except Exception:
            self.update_ui("", "Código inválido ou corrompido", True)

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # Gerenciar botão de voltar do Android
        Window.bind(on_keyboard=self.on_back_button)
        return CryptoScreen()

    def on_back_button(self, window, key, *args):
        if key == 27: # Tecla Back
            return False # Fecha o app graciosamente
        return False

if __name__ == '__main__':
    CryptoGuardApp().run()
