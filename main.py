import hashlib
import base64
import secrets
import string
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.config import Config

# REMOVE O MENU DE CONTEXTO PADRÃO DO KIVY
Config.set('kivy', 'textinput_selectable', '0') 

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        # Fundo Principal
        main_layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # HEADER COM ESTILO
        header = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing=dp(5))
        header.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H4", 
            bold=True, theme_text_color="Primary"
        ))
        header.add_widget(MDLabel(
            text="Segurança Minimalista", halign="center", font_style="Caption",
            theme_text_color="Secondary"
        ))
        main_layout.add_widget(header)

        # CARD CENTRAL (Efeito Glassmorphism)
        content_card = MDCard(
            orientation='vertical', padding=dp(15), spacing=dp(15),
            elevation=2, radius=[20,], md_bg_color=(0.12, 0.12, 0.15, 1),
            size_hint_y=None, height=dp(420)
        )

        # Campo Mensagem (Menu desativado)
        self.msg_input = MDTextField(
            hint_text="Mensagem para processar",
            mode="rectangle",
            multiline=True,
            input_type='text',
            use_bubble=False,  # REMOVE O MENU FEIO
            use_handles=False, # REMOVE AS BOLINHAS DE SELEÇÃO
            fill_color_normal=(0.08, 0.08, 0.1, 1),
        )
        content_card.add_widget(self.msg_input)

        # Container Senha com Revelar e Gerar
        pwd_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(60))
        
        self.pwd_input = MDTextField(
            hint_text="Chave Secreta",
            password=True,
            mode="rectangle",
            use_bubble=False,
            fill_color_normal=(0.08, 0.08, 0.1, 1),
        )
        
        # Botão Olhinho
        self.eye_btn = MDIconButton(
            icon="eye-off",
            on_release=self.toggle_visibility,
            pos_hint={"center_y": .5}
        )
        
        pwd_box.add_widget(self.pwd_input)
        pwd_box.add_widget(self.eye_btn)
        content_card.add_widget(pwd_box)

        # Botões de Ação de Alto Impacto
        actions = MDBoxLayout(spacing=dp(15), size_hint_y=None, height=dp(55))
        actions.add_widget(MDFillRoundFlatButton(
            text="🔒 PROTEGER", md_bg_color=(0.1, 0.4, 0.9, 1),
            size_hint_x=0.5, font_size=dp(16), on_release=self.encrypt
        ))
        actions.add_widget(MDFillRoundFlatButton(
            text="🔓 REVELAR", md_bg_color=(0.2, 0.2, 0.25, 1),
            size_hint_x=0.5, font_size=dp(16), on_release=self.decrypt
        ))
        content_card.add_widget(actions)

        # Área de Resultado em um Mini Card
        res_card = MDCard(
            radius=[15,], md_bg_color=(0.08, 0.08, 0.1, 1), 
            padding=dp(10), size_hint_y=None, height=dp(80)
        )
        scroll = ScrollView()
        self.result_label = MDLabel(
            text="Aguardando...", halign="center", 
            theme_text_color="Secondary", font_style="Caption"
        )
        scroll.add_widget(self.result_label)
        res_card.add_widget(scroll)
        content_card.add_widget(res_card)

        main_layout.add_widget(content_card)

        # TOOLBAR INFERIOR (Floating Style)
        toolbar = MDCard(
            radius=[25,], md_bg_color=(0.15, 0.15, 0.2, 1),
            adaptive_size=True, padding=[dp(20), dp(5)],
            pos_hint={"center_x": .5}, elevation=4
        )
        
        # Botões da Barra
        icons = [
            ("content-paste", self.paste_text),
            ("content-copy", self.copy_text),
            ("share-variant", self.share_text),
            ("key-plus", self.generate_pwd),
            ("delete-sweep", self.clear_fields)
        ]

        for icon, func in icons:
            toolbar.add_widget(MDIconButton(icon=icon, on_release=func, theme_text_color="Custom", icon_color=(1,1,1,1)))

        main_layout.add_widget(toolbar)
        self.add_widget(main_layout)

    def toggle_visibility(self, *args):
        self.pwd_input.password = not self.pwd_input.password
        self.eye_btn.icon = "eye" if not self.pwd_input.password else "eye-off"

    def paste_text(self, *args):
        self.msg_input.text = Clipboard.paste()

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
        self.pwd_input.text = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))

    def clear_fields(self, *args):
        self.msg_input.text = ""; self.pwd_input.text = ""; self.result_label.text = "Aguardando..."

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
