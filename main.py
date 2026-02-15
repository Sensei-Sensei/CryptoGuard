import hashlib
import base64
import secrets
import string
import threading
from kivy.config import Config

# Configurações de teclado ANTES de qualquer outro import do Kivy
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('graphics', 'resizable', '0')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform, mainthread

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        # Layout principal com padding seguro para notches de celular
        layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(40), dp(20), dp(20)], spacing=dp(15))
        
        # Header
        layout.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H5",
            bold=True, theme_text_color="Custom", text_color=(0, 0.8, 1, 1),
            size_hint_y=None, height=dp(50)
        ))

        # Card Central
        self.card = MDCard(
            orientation='vertical', padding=dp(15), spacing=dp(15),
            elevation=0, radius=[20,], md_bg_color=(1, 1, 1, 0.05),
            size_hint_y=None, height=dp(400), line_color=(1, 1, 1, 0.1)
        )

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

        # Botões
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

        # Resultado
        self.res_label = MDLabel(
            text="Pronto para uso", halign="center", 
            theme_text_color="Secondary", font_style="Caption"
        )
        self.card.add_widget(self.res_label)

        layout.add_widget(self.card)
        self.add_widget(layout)

    def show_toast(self, text, color=(0, 0.8, 1, 1)):
        Snackbar(text=text, bg_color=color, duration=2).open()

    @mainthread
    def update_ui(self, result, message, is_error=False):
        if not is_error:
            self.res_label.text = "Resultado copiado!"
            self.last_result = result
            Clipboard.copy(result)
            self.msg_input.text = "" # Limpa para segurança
        else:
            self.res_label.text = "Erro na operação."
        
        self.show_toast(message, (0.8, 0.2, 0.2, 1) if is_error else (0, 0.6, 0.4, 1))

    def start_encrypt(self, *args):
        threading.Thread(target=self._encrypt_logic, daemon=True).start()

    def _encrypt_logic(self):
        text = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()
        if not text or not pwd:
            self.update_ui("", "Preencha os campos!", True)
            return
        try:
            salt = secrets.token_bytes(16)
            # PBKDF2 é lento, por isso a Thread é essencial
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            nonce = secrets.token_bytes(8)
            data = nonce + text.encode('utf-8')
            
            expanded = b''
            for i in range((len(data) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            
            enc = bytes(a ^ b for a, b in zip(data, expanded))
            auth_tag = hashlib.sha256(key + enc).digest()[:16]
            final = base64.b64encode(salt + auth_tag + enc).decode()
            self.update_ui(final, "Criptografado!")
        except:
            self.update_ui("", "Erro interno", True)

    def start_decrypt(self, *args):
        threading.Thread(target=self._decrypt_logic, daemon=True).start()

    def _decrypt_logic(self):
        text = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()
        if not text or not pwd: return
        try:
            raw = base64.b64decode(text)
            salt, auth_tag, enc = raw[:16], raw[16:32], raw[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            
            if hashlib.sha256(key + enc).digest()[:16] != auth_tag:
                self.update_ui("", "Chave incorreta!", True)
                return

            expanded = b''
            for i in range((len(enc) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            
            res = bytes(a ^ b for a, b in zip(enc, expanded))[8:].decode('utf-8')
            self.update_ui(res, "Mensagem revelada!")
            self.msg_input.text = res # Mostra o texto original no campo
        except:
            self.update_ui("", "Código inválido", True)

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
