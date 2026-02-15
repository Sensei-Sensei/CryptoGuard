import hashlib
import base64
import secrets
import string
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Header
        layout.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H5", 
            bold=True, theme_text_color="Primary", size_hint_y=None, height=dp(50)
        ))

        # Campo Mensagem - Customizado para Seleção Bonita
        self.msg_input = MDTextField(
            hint_text="Mensagem",
            mode="fill",
            multiline=True,
            input_type='text',
            fill_color_normal=(0.1, 0.1, 0.13, 1),
            # Melhora o visual da seleção e do cursor
            cursor_color=(0.1, 0.5, 0.9, 1),
            selection_color=(0.1, 0.5, 0.9, 0.3) 
        )
        layout.add_widget(self.msg_input)

        # Container Senha
        pwd_container = MDRelativeLayout(size_hint_y=None, height=dp(60))
        self.pwd_input = MDTextField(
            hint_text="Chave Secreta",
            password=True,
            mode="fill",
            fill_color_normal=(0.1, 0.1, 0.13, 1),
            cursor_color=(0.1, 0.5, 0.9, 1)
        )
        self.eye_btn = MDIconButton(
            icon="eye-off", pos_hint={"center_y": .5, "right": 1},
            on_release=self.toggle_visibility
        )
        pwd_container.add_widget(self.pwd_input)
        pwd_container.add_widget(self.eye_btn)
        layout.add_widget(pwd_container)

        # Botões
        btns = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        btns.add_widget(MDRaisedButton(
            text="PROTEGER", md_bg_color=(0.1, 0.5, 0.9, 1),
            size_hint_x=0.5, on_release=self.encrypt
        ))
        btns.add_widget(MDRaisedButton(
            text="REVELAR", md_bg_color=(0.2, 0.2, 0.25, 1),
            size_hint_x=0.5, on_release=self.decrypt
        ))
        layout.add_widget(btns)

        # Resultado
        scroll = ScrollView()
        self.result_label = MDLabel(
            text="Aguardando...", halign="center", theme_text_color="Secondary",
            font_style="Body2", size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)

        # Toolbar
        toolbar = MDBoxLayout(spacing=dp(15), adaptive_size=True, pos_hint={"center_x": .5})
        toolbar.add_widget(MDIconButton(icon="content-copy", on_release=self.copy_text))
        toolbar.add_widget(MDIconButton(icon="share-variant", on_release=self.share_text))
        toolbar.add_widget(MDIconButton(icon="key-plus", on_release=self.generate_pwd))
        toolbar.add_widget(MDIconButton(icon="delete-sweep", on_release=self.clear_fields))
        layout.add_widget(toolbar)

        self.add_widget(layout)

    def toggle_visibility(self, *args):
        self.pwd_input.password = not self.pwd_input.password
        self.eye_btn.icon = "eye" if not self.pwd_input.password else "eye-off"

    def encrypt(self, *args):
        text, pwd = self.msg_input.text.strip(), self.pwd_input.text.strip()
        if not text or not pwd: return
        try:
            salt = secrets.token_bytes(16)
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            nonce = secrets.token_bytes(8)
            combined = nonce + text.encode('utf-8')
            expanded = b''
            counter = 0
            while len(expanded) < len(combined):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            enc = bytes(a ^ b for a, b in zip(combined, expanded[:len(combined)]))
            final = base64.b64encode(salt + hashlib.sha256(key + enc).digest()[:16] + enc).decode()
            self.result_label.text = final
            self.last_result = final
        except Exception as e: self.result_label.text = str(e)

    def decrypt(self, *args):
        text, pwd = self.msg_input.text.strip(), self.pwd_input.text.strip()
        try:
            data = base64.b64decode(text)
            salt, hmac_rec, enc = data[:16], data[16:32], data[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            if hashlib.sha256(key + enc).digest()[:16] != hmac_rec:
                self.result_label.text = "Chave Errada!"
                return
            expanded = b''
            counter = 0
            while len(expanded) < len(enc):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            res = bytes(a ^ b for a, b in zip(enc, expanded[:len(enc)]))[8:].decode('utf-8')
            self.result_label.text = res
            self.last_result = res
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
        if self.last_result: Clipboard.copy(self.last_result)

    def generate_pwd(self, *args):
        new_pwd = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        self.pwd_input.text = new_pwd

    def clear_fields(self, *args):
        self.msg_input.text = ""; self.pwd_input.text = ""; self.result_label.text = "Aguardando..."

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
