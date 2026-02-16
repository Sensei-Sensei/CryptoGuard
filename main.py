import hashlib
import base64
import secrets
import threading

# Tente configurar o Kivy antes de qualquer outra coisa
try:
    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'system')
    
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
except ImportError as e:
    print(f"Erro ao carregar módulos: {e}")

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(40), dp(20), dp(20)], spacing=dp(15))
        
        layout.add_widget(MDLabel(
            text="CRYPTO GUARD", halign="center", font_style="H5",
            bold=True, theme_text_color="Custom", text_color=(0, 0.8, 1, 1),
            size_hint_y=None, height=dp(50)
        ))

        self.card = MDCard(
            orientation='vertical', padding=dp(15), spacing=dp(15),
            elevation=0, radius=[dp(20),], md_bg_color=(1, 1, 1, 0.05),
            size_hint_y=None, height=dp(420), line_color=(1, 1, 1, 0.1)
        )

        self.msg_input = MDTextField(hint_text="Mensagem ou Código", mode="rectangle", multiline=True)
        self.pwd_input = MDTextField(hint_text="Chave de Acesso", password=True, mode="rectangle")
        
        self.card.add_widget(self.msg_input)
        self.card.add_widget(self.pwd_input)

        btns = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        btns.add_widget(MDFillRoundFlatIconButton(icon="shield-lock", text="PROTEGER", on_release=self.start_encrypt, size_hint_x=0.5))
        btns.add_widget(MDFillRoundFlatIconButton(icon="lock-open", text="REVELAR", on_release=self.start_decrypt, size_hint_x=0.5))
        
        self.card.add_widget(btns)
        self.res_label = MDLabel(text="Pronto", halign="center", theme_text_color="Secondary", font_style="Caption")
        self.card.add_widget(self.res_label)

        layout.add_widget(self.card)
        layout.add_widget(MDBoxLayout())
        self.add_widget(layout)

    @mainthread
    def update_ui(self, result, info, is_error=False):
        self.res_label.text = info
        if not is_error and result:
            Clipboard.copy(result)
            if "Criptografado" in info: self.msg_input.text = ""
            else: self.msg_input.text = result
        Snackbar(text=info, bg_color=((0.8, 0.2, 0.2, 1) if is_error else (0, 0.6, 0.4, 1))).open()

    def start_encrypt(self, *args):
        threading.Thread(target=self._encrypt_task, daemon=True).start()

    def _encrypt_task(self):
        msg, pwd = self.msg_input.text.strip(), self.pwd_input.text.strip()
        if not msg or not pwd:
            self.update_ui("", "Preencha tudo!", True)
            return
        try:
            salt = secrets.token_bytes(16)
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            nonce = secrets.token_bytes(8)
            data = nonce + msg.encode('utf-8')
            expanded = b''
            for i in range((len(data) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            enc = bytes(a ^ b for a, b in zip(data, expanded))
            auth_tag = hashlib.sha256(key + enc).digest()[:16]
            final = base64.b64encode(salt + auth_tag + enc).decode()
            self.update_ui(final, "Criptografado e Copiado!")
        except Exception as e:
            self.update_ui("", f"Erro: {str(e)}", True)

    def start_decrypt(self, *args):
        threading.Thread(target=self._decrypt_task, daemon=True).start()

    def _decrypt_task(self):
        code, pwd = self.msg_input.text.strip(), self.pwd_input.text.strip()
        if not code or not pwd: return
        try:
            raw = base64.b64decode(code)
            salt, auth_tag, enc = raw[:16], raw[16:32], raw[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            if hashlib.sha256(key + enc).digest()[:16] != auth_tag:
                self.update_ui("", "Chave incorreta!", True)
                return
            expanded = b''
            for i in range((len(enc) // 32) + 1):
                expanded += hashlib.sha256(key + i.to_bytes(4, 'big')).digest()
            res = bytes(a ^ b for a, b in zip(enc, expanded))[8:].decode('utf-8')
            self.update_ui(res, "Mensagem Revelada!")
        except:
            self.update_ui("", "Código inválido", True)

class CryptoGuardApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return CryptoScreen()

if __name__ == '__main__':
    CryptoGuardApp().run()
