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
from kivy.clock import Clock

# Força o sistema de teclado mais estável para evitar letras pulando
Config.set('kivy', 'keyboard_mode', 'system')

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        main_layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(40), dp(20), dp(20)], spacing=dp(20))
        
        # Header
        main_layout.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H5",
            bold=True, theme_text_color="Custom", text_color=(0, 0.8, 1, 1),
            size_hint_y=None, height=dp(40)
        ))

        # Card de Conteúdo
        self.content_card = MDCard(
            orientation='vertical', padding=dp(15), spacing=dp(10),
            elevation=0, radius=[20,], md_bg_color=(1, 1, 1, 0.05),
            size_hint_y=None, height=dp(420), line_color=(1, 1, 1, 0.1)
        )

        # Campo Mensagem (Correção de Digitação e Performance)
        self.msg_input = MDTextField(
            hint_text="Mensagem Secreta", mode="rectangle", multiline=True,
            use_bubble=False, fill_color_normal=(1, 1, 1, 0.02),
            input_type='text', keyboard_suggestions=False, # Impede o bug das letras
            line_color_focus=(0, 0.8, 1, 1)
        )
        self.content_card.add_widget(self.msg_input)

        # Campo Senha
        pwd_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(60))
        self.pwd_input = MDTextField(
            hint_text="Chave de Acesso", password=True, mode="rectangle",
            use_bubble=False, line_color_focus=(0, 0.8, 1, 1),
            fill_color_normal=(1, 1, 1, 0.02), keyboard_suggestions=False
        )
        self.eye_btn = MDIconButton(
            icon="eye-off", on_release=self.toggle_visibility, 
            pos_hint={"center_y": .5}, theme_text_color="Custom", icon_color=(0, 0.8, 1, 1)
        )
        pwd_box.add_widget(self.pwd_input); pwd_box.add_widget(self.eye_btn)
        self.content_card.add_widget(pwd_box)

        # Botões
        actions = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        actions.add_widget(MDFillRoundFlatIconButton(
            icon="shield-lock", text="PROTEGER", md_bg_color=(0, 0.4, 0.8, 1),
            size_hint_x=0.5, on_release=self.encrypt
        ))
        actions.add_widget(MDFillRoundFlatIconButton(
            icon="lock-open-variant", text="REVELAR", md_bg_color=(0.15, 0.15, 0.18, 1),
            size_hint_x=0.5, on_release=self.decrypt
        ))
        self.content_card.add_widget(actions)

        # Área de Resultado
        res_container = MDCard(
            radius=[15,], md_bg_color=(0, 0, 0, 0.3), padding=dp(8), 
            size_hint_y=None, height=dp(80), line_color=(1, 1, 1, 0.05)
        )
        scroll = ScrollView()
        self.result_label = MDLabel(
            text="Pronto.", halign="center", 
            theme_text_color="Secondary", font_style="Caption", size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label); res_container.add_widget(scroll)
        self.content_card.add_widget(res_container)

        main_layout.add_widget(self.content_card)

        # Toolbar
        self.toolbar = MDCard(
            radius=[25,], md_bg_color=(0.1, 0.1, 0.12, 0.95),
            adaptive_size=True, padding=[dp(10), dp(2)],
            pos_hint={"center_x": .5}, elevation=2
        )
        for icon, func in [("content-paste", self.paste_text), ("content-copy", self.copy_text), 
                           ("share-variant", self.share_text), ("key-plus", self.generate_pwd), 
                           ("delete-sweep", self.clear_fields)]:
            self.toolbar.add_widget(MDIconButton(icon=icon, on_release=func, theme_text_color="Custom", icon_color=(0, 0.8, 1, 1)))

        main_layout.add_widget(self.toolbar)
        self.add_widget(main_layout)

    def show_toast(self, text, color=(0, 0.8, 1, 1)):
        # Snackbars são assíncronos e não travam o app
        Clock.schedule_once(lambda dt: Snackbar(text=text, bg_color=color, duration=2, margin=dp(15), radius=[10]).open())

    def toggle_visibility(self, *args):
        self.pwd_input.password = not self.pwd_input.password
        self.eye_btn.icon = "eye" if not self.pwd_input.password else "eye-off"

    def encrypt(self, *args):
        text, pwd = self.msg_input.text.strip(), self.pwd_input.text.strip()
        if not text or not pwd:
            self.show_toast("Campos vazios!", (0.8, 0.2, 0.2, 1))
            return
        
        try:
            salt = secrets.token_bytes(16)
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            nonce = secrets.token_bytes(8)
            data = nonce + text.encode('utf-8')
            
            # XOR Stream Cipher simples para performance
            expanded = b''
            for i in range((len(data) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            
            enc = bytes(a ^ b for a, b in zip(data, expanded))
            auth_tag = hashlib.sha256(key + enc).digest()[:16]
            final = base64.b64encode(salt + auth_tag + enc).decode()
            
            self.result_label.text = final
            self.last_result = final
            Clipboard.copy(final)
            self.show_toast("Criptografado e Copiado!")
        except Exception as e:
            self.show_toast("Erro ao processar", (0.8, 0.2, 0.2, 1))

    def decrypt(self, *args):
        text, pwd = self.msg_input.text.strip(), self.pwd_input.text.strip()
        if not text or not pwd: return
        
        try:
            raw = base64.b64decode(text)
            salt, auth_tag, enc = raw[:16], raw[16:32], raw[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            
            # VERIFICAÇÃO DE SENHA (AQUI ESTAVA O PROBLEMA)
            if hashlib.sha256(key + enc).digest()[:16] != auth_tag:
                self.show_toast("SENHA INCORRETA!", (0.8, 0.2, 0.2, 1))
                self.result_label.text = "Acesso Negado."
                return

            expanded = b''
            for i in range((len(enc) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            
            res = bytes(a ^ b for a, b in zip(enc, expanded))[8:].decode('utf-8')
            self.result_label.text = res
            self.last_result = res
            self.show_toast("Mensagem Revelada!")
        except:
            self.show_toast("CÓDIGO INVÁLIDO!", (0.8, 0.2, 0.2, 1))

    def paste_text(self, *args):
        self.msg_input.text = Clipboard.paste()
    
    def copy_text(self, *args):
        if self.last_result: 
            Clipboard.copy(self.last_result)
            self.show_toast("Copiado!")

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
            PythonActivity.mActivity.startActivity(Intent.createChooser(intent, String("Enviar")))

    def generate_pwd(self, *args):
        new_pwd = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        self.pwd_input.text = new_pwd
        self.show_toast("Chave sugerida gerada!")

    def clear_fields(self, *args):
        self.msg_input.text = ""; self.pwd_input.text = ""; self.result_label.text = "Pronto."

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
