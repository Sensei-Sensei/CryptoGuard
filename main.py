import hashlib
import base64
import secrets
import string
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFillRoundFlatIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivy.config import Config

# Desativa menus de contexto antigos para manter a UI limpa
Config.set('kivy', 'textinput_selectable', '0')

class CryptoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = ""
        
        # Layout principal com padding extra no topo para evitar "letras emboladas"
        main_layout = MDBoxLayout(orientation='vertical', padding=[dp(20), dp(50), dp(20), dp(20)], spacing=dp(20))
        
        # Header - Título único e limpo
        main_layout.add_widget(MDLabel(
            text="CRYPTO GUARD",
            halign="center",
            font_style="H5",
            bold=True,
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40)
        ))

        # Card de Conteúdo
        content_card = MDCard(
            orientation='vertical', padding=dp(20), spacing=dp(15),
            elevation=2, radius=[20,], md_bg_color=(0.12, 0.12, 0.15, 1),
            size_hint_y=None, height=dp(420)
        )

        # Campo Mensagem - CONFIGURADO PARA CORRETOR ORTOGRÁFICO
        self.msg_input = MDTextField(
            hint_text="Mensagem para processar",
            mode="rectangle",
            multiline=True,
            use_bubble=False,
            fill_color_normal=(0.08, 0.08, 0.1, 1),
            # Ativa o corretor ortográfico no Android:
            input_type='text',
            input_filter=None,
            keyboard_suggestions=True
        )
        content_card.add_widget(self.msg_input)

        # Container Senha com Revelar
        pwd_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(60))
        self.pwd_input = MDTextField(
            hint_text="Chave Secreta",
            password=True,
            mode="rectangle",
            use_bubble=False,
            fill_color_normal=(0.08, 0.08, 0.1, 1),
            input_type='text' # Permite que o teclado mostre sugestões mesmo em senha
        )
        self.eye_btn = MDIconButton(
            icon="eye-off",
            on_release=self.toggle_visibility,
            pos_hint={"center_y": .5}
        )
        pwd_box.add_widget(self.pwd_input)
        pwd_box.add_widget(self.eye_btn)
        content_card.add_widget(pwd_box)

        # Botões de Ação com Ícones (Sem Emojis que causam erro)
        actions = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        actions.add_widget(MDFillRoundFlatIconButton(
            icon="lock", text="PROTEGER", md_bg_color=(0.1, 0.5, 0.9, 1),
            size_hint_x=0.5, on_release=self.encrypt
        ))
        actions.add_widget(MDFillRoundFlatIconButton(
            icon="lock-open-variant", text="REVELAR", md_bg_color=(0.2, 0.2, 0.25, 1),
            size_hint_x=0.5, on_release=self.decrypt
        ))
        content_card.add_widget(actions)

        # Área de Resultado
        res_card = MDCard(
            radius=[15,], md_bg_color=(0.08, 0.08, 0.1, 1), 
            padding=dp(10), size_hint_y=None, height=dp(100)
        )
        scroll = ScrollView()
        self.result_label = MDLabel(
            text="Aguardando...", halign="center", 
            theme_text_color="Secondary", font_style="Caption", size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        res_card.add_widget(scroll)
        content_card.add_widget(res_card)

        main_layout.add_widget(content_card)

        # Toolbar Inferior
        toolbar = MDCard(
            radius=[25,], md_bg_color=(0.15, 0.15, 0.2, 1),
            adaptive_size=True, padding=[dp(15), dp(5)],
            pos_hint={"center_x": .5}, elevation=4
        )
        toolbar.add_widget(MDIconButton(icon="content-paste", on_release=self.paste_text))
        toolbar.add_widget(MDIconButton(icon="content-copy", on_release=self.copy_text))
        toolbar.add_widget(MDIconButton(icon="share-variant", on_release=self.share_text))
        toolbar.add_widget(MDIconButton(icon="key-plus", on_release=self.generate_pwd))
        toolbar.add_widget(MDIconButton(icon="delete-sweep", on_release=self.clear_fields))

        main_layout.add_widget(toolbar)
        self.add_widget(main_layout)

    def toggle_visibility(self, *args):
        self.pwd_input.password = not self.pwd_input.password
        self.eye_btn.icon = "eye" if not self.pwd_input.password else "eye-off"

    def paste_text(self, *args):
        self.msg_input.text = Clipboard.paste()

    def generate_pwd(self, *args):
        new_pwd = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        self.pwd_input.text = new_pwd
        self.last_result = new_pwd
        Clipboard.copy(new_pwd) # Copia automaticamente ao gerar
        self.result_label.text = f"CHAVE COPIADA: {new_pwd}"

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
            Clipboard.copy(final) # Copia automaticamente o resultado
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
