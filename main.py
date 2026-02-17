import hashlib
import base64
import secrets
import string
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.config import Config

# Desativa seleções automáticas que podem causar crash em campos multiline
Config.set('kivy', 'textinput_selectable', '0')

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        main_layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(50), dp(20), dp(20)], spacing=dp(20))
        
        main_layout.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H5",
            bold=True, theme_text_color="Primary", size_hint_y=None, height=dp(40)
        ))

        content_card = MDCard(
            orientation='vertical', padding=dp(15), spacing=dp(15),
            elevation=2, radius=[dp(20),], size_hint_y=None, height=dp(450)
        )

        # CORREÇÃO DO TECLADO: spellcheck=False e input_type='mail' evitam o erro de texto embaralhado
        self.msg_input = MDTextField(
            hint_text="Sua mensagem ou código",
            mode="rectangle", 
            multiline=True, 
            size_hint_y=None, 
            height=dp(100),
            spellcheck=False, # Desativa o corretor ortográfico
            input_type='mail'  # Sugere ao teclado não usar predição agressiva
        )
        
        self.pwd_input = MDTextField(
            hint_text="Chave de Acesso",
            mode="rectangle", 
            password=True, 
            size_hint_y=None, 
            height=dp(50),
            spellcheck=False
        )

        content_card.add_widget(self.msg_input)
        content_card.add_widget(self.pwd_input)

        btn_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        # Botões arredondados (conforme seu modelo original)
        self.encrypt_btn = MDFillRoundFlatIconButton(
            icon="shield-lock", text="PROTEGER",
            radius=[dp(25), dp(25), dp(25), dp(25)],
            on_release=self.encrypt_text, size_hint_x=0.5
        )
        
        self.decrypt_btn = MDFillRoundFlatIconButton(
            icon="lock-open", text="REVELAR",
            radius=[dp(25), dp(25), dp(25), dp(25)],
            on_release=self.decrypt_text, size_hint_x=0.5
        )

        btn_box.add_widget(self.encrypt_btn)
        btn_box.add_widget(self.decrypt_btn)
        content_card.add_widget(btn_box)

        self.result_label = MDLabel(
            text="Aguardando...", halign="center",
            theme_text_color="Secondary", font_style="Caption"
        )
        content_card.add_widget(self.result_label)

        extra_box = MDBoxLayout(spacing=dp(20), adaptive_size=True, pos_hint={"center_x": .5})
        extra_box.add_widget(MDIconButton(icon="content-copy", on_release=self.copy_text))
        extra_box.add_widget(MDIconButton(icon="share-variant", on_release=self.share_text))
        extra_box.add_widget(MDIconButton(icon="delete-outline", on_release=self.clear_fields))
        
        content_card.add_widget(extra_box)
        main_layout.add_widget(content_card)
        main_layout.add_widget(MDBoxLayout()) 
        self.add_widget(main_layout)

    def encrypt_text(self, *args):
        msg = self.msg_input.text.strip(); pwd = self.pwd_input.text.strip()
        if not msg or not pwd: return
        try:
            salt = secrets.token_bytes(16)
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            nonce = secrets.token_bytes(8)
            data = nonce + msg.encode('utf-8')
            expanded = b''
            counter = 0
            while len(expanded) < len(data):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            enc = bytes(a ^ b for a, b in zip(data, expanded[:len(data)]))
            auth_tag = hashlib.sha256(key + enc).digest()[:16]
            final = base64.b64encode(salt + auth_tag + enc).decode()
            self.result_label.text = "Criptografado!"
            self.last_result = final
            self.msg_input.text = ""
        except: self.result_label.text = "Erro!"

    def decrypt_text(self, *args):
        code = self.msg_input.text.strip(); pwd = self.pwd_input.text.strip()
        if not code or not pwd: return
        try:
            raw = base64.b64decode(code)
            salt, auth_tag, enc = raw[:16], raw[16:32], raw[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            if hashlib.sha256(key + enc).digest()[:16] != auth_tag:
                self.result_label.text = "Chave Errada!"
                return
            expanded = b''
            counter = 0
            while len(expanded) < len(enc):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            res = bytes(a ^ b for a, b in zip(enc, expanded[:len(enc)]))[8:].decode('utf-8')
            self.result_label.text = "Revelado!"
            self.last_result = res
            self.msg_input.text = res
        except: self.result_label.text = "Código Inválido!"

    def share_text(self, *args):
        if not self.last_result: return
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")
            intent.putExtra(Intent.EXTRA_TEXT, String(self.last_result))
            PythonActivity.mActivity.startActivity(Intent.createChooser(intent, String("Enviar:")))
        else: Clipboard.copy(self.last_result)

    def copy_text(self, *args):
        if self.last_result: 
            Clipboard.copy(self.last_result)
            self.result_label.text = "Copiado!"

    def clear_fields(self, *args):
        self.msg_input.text = ""; self.pwd_input.text = ""; self.result_label.text = "Aguardando..."

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
