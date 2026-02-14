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
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        # Layout Principal
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Título
        layout.add_widget(MDLabel(
            text="CRYPTO GUARD",
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(50)
        ))

        # Campo de Mensagem
        self.msg_input = MDTextField(
            hint_text="Mensagem secreta",
            helper_text="Digite o texto que deseja proteger ou revelar",
            helper_text_mode="on_focus",
            mode="fill",
            multiline=True,
            fill_color_normal=(0.1, 0.1, 0.13, 1)
        )
        layout.add_widget(self.msg_input)

        # Campo de Senha
        self.pwd_input = MDTextField(
            hint_text="Chave de segurança",
            password=True,
            mode="fill",
            fill_color_normal=(0.1, 0.1, 0.13, 1)
        )
        layout.add_widget(self.pwd_input)

        # Botões de Ação
        actions = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        btn_enc = MDRaisedButton(
            text="PROTEGER",
            md_bg_color=(0.1, 0.5, 0.9, 1),
            size_hint_x=0.5,
            on_release=self.encrypt
        )
        btn_dec = MDRaisedButton(
            text="REVELAR",
            md_bg_color=(0.2, 0.2, 0.25, 1),
            size_hint_x=0.5,
            on_release=self.decrypt
        )
        actions.add_widget(btn_enc)
        actions.add_widget(btn_dec)
        layout.add_widget(actions)

        # Área de Resultado
        scroll = ScrollView(size_hint=(1, 0.3))
        self.result_label = MDLabel(
            text="Aguardando operação...",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)

        # Barra de Ferramentas com Ícones (Emojis Profissionais)
        toolbar = MDBoxLayout(spacing=dp(10), adaptive_size=True, pos_hint={"center_x": .5})
        toolbar.add_widget(MDIconButton(icon="content-copy", on_release=self.copy_text))
        toolbar.add_widget(MDIconButton(icon="share-variant", on_release=self.share_text))
        toolbar.add_widget(MDIconButton(icon="key-plus", on_release=self.generate_pwd))
        toolbar.add_widget(MDIconButton(icon="delete-sweep", on_release=self.clear_fields))
        layout.add_widget(toolbar)

        self.add_widget(layout)

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
            encrypted = bytes(a ^ b for a, b in zip(combined, expanded))
            final = base64.b64encode(salt + hashlib.sha256(key + encrypted).digest()[:16] + encrypted).decode()
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
                self.result_label.text = "Chave Incorreta!"
                return
            expanded = b''
            counter = 0
            while len(expanded) < len(enc):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            original = bytes(a ^ b for a, b in zip(enc, expanded))[8:].decode('utf-8')
            self.result_label.text = original
            self.last_result = original
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
            PythonActivity.mActivity.startActivity(Intent.createChooser(intent, String("Compartilhar")))
        else:
            Clipboard.copy(self.last_result)

    def copy_text(self, *args):
        if self.last_result:
            Clipboard.copy(self.last_result)

    def generate_pwd(self, *args):
        pwd = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        self.pwd_input.text = pwd

    def clear_fields(self, *args):
        self.msg_input.text = ""
        self.pwd_input.text = ""
        self.result_label.text = "Aguardando operação..."
        self.last_result = ""

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
