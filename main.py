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
from kivymd.uix.snackbar import Snackbar
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.config import Config

# Desativa menus nativos que causam instabilidade
Config.set('kivy', 'textinput_selectable', '0')

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        main_layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(50), dp(20), dp(20)], spacing=dp(25))
        
        # Header Neon
        main_layout.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H5",
            bold=True, theme_text_color="Custom", text_color=(0, 0.8, 1, 1),
            size_hint_y=None, height=dp(40)
        ))

        # Card Central (Glassmorphism)
        self.content_card = MDCard(
            orientation='vertical', padding=dp(20), spacing=dp(15),
            elevation=0, radius=[25,], md_bg_color=(1, 1, 1, 0.05),
            size_hint_y=None, height=dp(440), line_color=(1, 1, 1, 0.1)
        )

        self.msg_input = MDTextField(
            hint_text="Mensagem Secreta", mode="rectangle", multiline=True,
            use_bubble=False, use_handles=False, fill_color_normal=(1, 1, 1, 0.02),
            input_type='text', line_color_focus=(0, 0.8, 1, 1)
        )
        self.content_card.add_widget(self.msg_input)

        pwd_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(60))
        self.pwd_input = MDTextField(
            hint_text="Chave de Acesso", password=True, mode="rectangle",
            use_bubble=False, line_color_focus=(0, 0.8, 1, 1),
            fill_color_normal=(1, 1, 1, 0.02)
        )
        self.eye_btn = MDIconButton(
            icon="eye-off", on_release=self.toggle_visibility, 
            pos_hint={"center_y": .5}, theme_text_color="Custom", icon_color=(0, 0.8, 1, 1)
        )
        pwd_box.add_widget(self.pwd_input); pwd_box.add_widget(self.eye_btn)
        self.content_card.add_widget(pwd_box)

        actions = MDBoxLayout(spacing=dp(12), size_hint_y=None, height=dp(55))
        actions.add_widget(MDFillRoundFlatIconButton(
            icon="shield-lock", text="PROTEGER", md_bg_color=(0, 0.4, 0.8, 1),
            size_hint_x=0.5, on_release=self.encrypt
        ))
        actions.add_widget(MDFillRoundFlatIconButton(
            icon="lock-open-variant", text="REVELAR", md_bg_color=(0.15, 0.15, 0.18, 1),
            size_hint_x=0.5, on_release=self.decrypt
        ))
        self.content_card.add_widget(actions)

        res_container = MDCard(
            radius=[15,], md_bg_color=(0, 0, 0, 0.3), padding=dp(10), 
            size_hint_y=None, height=dp(100), line_color=(1, 1, 1, 0.05)
        )
        scroll = ScrollView()
        self.result_label = MDLabel(
            text="Aguardando...", halign="center", 
            theme_text_color="Secondary", font_style="Caption", size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label); res_container.add_widget(scroll)
        self.content_card.add_widget(res_container)

        main_layout.add_widget(self.content_card)

        # Toolbar Inferior
        self.toolbar = MDCard(
            radius=[30,], md_bg_color=(0.1, 0.1, 0.12, 0.9),
            adaptive_size=True, padding=[dp(15), dp(5)],
            pos_hint={"center_x": .5}, elevation=4
        )
        for icon, func in [("content-paste", self.paste_text), ("content-copy", self.copy_text), 
                           ("share-variant", self.share_text), ("key-plus", self.generate_pwd), 
                           ("delete-sweep", self.clear_fields)]:
            self.toolbar.add_widget(MDIconButton(icon=icon, on_release=func, theme_text_color="Custom", icon_color=(0, 0.8, 1, 1)))

        main_layout.add_widget(self.toolbar)
        self.add_widget(main_layout)

    def show_toast(self, text, color=(0, 0.8, 1, 1)):
        try:
            Snackbar(text=text, bg_color=color, duration=2, radius=[15,], margin=dp(15)).open()
        except: pass

    def toggle_visibility(self, *args):
        self.pwd_input.password = not self.pwd_input.password
        self.eye_btn.icon = "eye" if not self.pwd_input.password else "eye-off"

    def paste_text(self, *args):
        self.msg_input.text = Clipboard.paste()
        self.show_toast("Texto colado!")

    def generate_pwd(self, *args):
        new_pwd = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        self.pwd_input.text = new_pwd
        Clipboard.copy(new_pwd)
        self.show_toast("Chave gerada e copiada!")

    def encrypt(self, *args):
        text = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()
        if not text or not pwd:
            self.show_toast("Preencha os campos!", color=(0.8, 0.2, 0.2, 1))
            return
        
        try:
            # PBKDF2 + AES-Style XOR
            salt = secrets.token_bytes(16)
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            nonce = secrets.token_bytes(8)
            data_bytes = nonce + text.encode('utf-8')
            
            # Expansão de chave segura
            expanded = b''
            counter = 0
            while len(expanded) < len(data_bytes):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            
            enc = bytes(a ^ b for a, b in zip(data_bytes, expanded))
            auth_tag = hashlib.sha256(key + enc).digest()[:16]
            final = base64.b64encode(salt + auth_tag + enc).decode()
            
            self.result_label.text = final
            self.last_result = final
            Clipboard.copy(final)
            self.show_toast("Protegido e Copiado!")
        except Exception as e:
            self.show_toast(f"Erro no processamento", color=(0.8, 0.2, 0.2, 1))

    def decrypt(self, *args):
        text = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()
        if not text or not pwd: return
        
        try:
            raw = base64.b64decode(text)
            salt, auth_tag, enc = raw[:16], raw[16:32], raw[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            
            if hashlib.sha256(key + enc).digest()[:16] != auth_tag:
                self.show_toast("Chave Incorreta!", color=(0.8, 0.2, 0.2, 1))
                return

            expanded = b''
            counter = 0
            while len(expanded) < len(enc):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            
            res = bytes(a ^ b for a, b in zip(enc, expanded))[8:].decode('utf-8')
            self.result_label.text = res
            self.last_result = res
            self.show_toast("Revelado!")
        except:
            self.show_toast("Falha na decodificação", color=(0.8, 0.2, 0.2, 1))

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
        else: Clipboard.copy(self.last_result)

    def copy_text(self, *args):
        if self.last_result:
            Clipboard.copy(self.last_result)
            self.show_toast("Copiado!")

    def clear_fields(self, *args):
        self.msg_input.text = ""; self.pwd_input.text = ""; self.result_label.text = "Aguardando..."

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
