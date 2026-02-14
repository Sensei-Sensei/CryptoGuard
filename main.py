import hashlib
import base64
import secrets
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.window import Window

# Cores do Tema Minimalista Dark
BG_COLOR = (0.02, 0.02, 0.03, 1)  # Quase preto
CARD_COLOR = (0.07, 0.07, 0.1, 1) # Cinza azulado escuro
ACCENT_COLOR = (0.12, 0.58, 0.95, 1) # Azul Moderno
TEXT_COLOR = (0.95, 0.95, 0.95, 1)

Window.clearcolor = BG_COLOR

class CryptoGuard(App):
    def build(self):
        self.title = 'CryptoGuard'
        self.last_result = ""
        
        # Layout Principal com respiro (padding)
        root = BoxLayout(orientation='vertical', padding=dp(25), spacing=dp(15))
        
        # TÍTULO MINIMALISTA
        header = Label(
            text='Crypto[b]Guard[/b]',
            markup=True,
            font_size=dp(30),
            size_hint=(1, 0.1),
            color=ACCENT_COLOR
        )
        root.add_widget(header)
        
        # INPUT DE MENSAGEM (ESTILO CARD)
        self.msg_input = TextInput(
            hint_text='Digite ou cole o texto aqui...',
            multiline=True,
            size_hint=(1, 0.2),
            font_size=dp(16),
            background_normal='',
            background_color=CARD_COLOR,
            foreground_color=TEXT_COLOR,
            padding=[dp(15), dp(15)],
            cursor_color=ACCENT_COLOR,
            hint_text_color=(0.4, 0.4, 0.5, 1)
        )
        root.add_widget(self.msg_input)
        
        # INPUT DE SENHA
        self.pwd_input = TextInput(
            hint_text='Sua chave secreta 🔑',
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            font_size=dp(16),
            background_normal='',
            background_color=CARD_COLOR,
            foreground_color=TEXT_COLOR,
            padding=[dp(15), dp(13)],
            cursor_color=ACCENT_COLOR
        )
        root.add_widget(self.pwd_input)
        
        # BOTÕES DE AÇÃO (LADO A LADO)
        btn_box = BoxLayout(size_hint=(1, 0.1), spacing=dp(10))
        
        self.btn_enc = Button(
            text='🔒 PROTEGER',
            background_normal='',
            background_color=ACCENT_COLOR,
            bold=True,
            font_size=dp(14)
        )
        self.btn_enc.bind(on_press=self.encrypt)
        
        self.btn_dec = Button(
            text='🔓 REVELAR',
            background_normal='',
            background_color=(0.2, 0.2, 0.25, 1),
            bold=True,
            font_size=dp(14)
        )
        self.btn_dec.bind(on_press=self.decrypt)
        
        btn_box.add_widget(self.btn_enc)
        btn_box.add_widget(self.btn_dec)
        root.add_widget(btn_box)
        
        # ÁREA DE RESULTADO
        scroll = ScrollView(size_hint=(1, 0.25))
        self.result_label = Label(
            text='Aguardando...',
            size_hint_y=None,
            font_size=dp(15),
            color=(0.7, 0.7, 0.8, 1),
            halign='center'
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_label.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)

        # UTILITÁRIOS (BOTÃO DE COMPARTILHAR ADICIONADO)
        util_box = BoxLayout(size_hint=(1, 0.08), spacing=dp(8))
        
        btns_data = [
            ('📋 Copiar', self.copy_text, (0.15, 0.15, 0.2, 1)),
            ('📤 Enviar', self.share_text, (0.1, 0.4, 0.2, 1)),
            ('🎲 Senha', self.generate_password, (0.15, 0.15, 0.2, 1)),
            ('🧹', self.clear_fields, (0.4, 0.1, 0.1, 1))
        ]

        for text, func, color in btns_data:
            b = Button(text=text, background_normal='', background_color=color, font_size=dp(12))
            b.bind(on_press=func)
            util_box.add_widget(b)
            
        root.add_widget(util_box)
        return root

    def encrypt(self, instance):
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
        except Exception as e: self.show_popup('Erro', str(e))

    def decrypt(self, instance):
        text, pwd = self.msg_input.text.strip(), self.pwd_input.text.strip()
        try:
            data = base64.b64decode(text)
            salt, hmac_rec, enc = data[:16], data[16:32], data[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            if hashlib.sha256(key + enc).digest()[:16] != hmac_rec:
                self.show_popup('🚫', 'Chave Incorreta!')
                return
            expanded = b''
            counter = 0
            while len(expanded) < len(enc):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            original = bytes(a ^ b for a, b in zip(enc, expanded))[8:].decode('utf-8')
            self.result_label.text = original
            self.last_result = original
        except: self.show_popup('⚠️', 'Código Inválido!')

    def generate_password(self, instance):
        pwd = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        self.pwd_input.text = pwd
        self.show_popup('🔑 Senha', f'Nova senha criada:\n{pwd}')

    def share_text(self, instance):
        if not self.last_result:
            self.show_popup('⚠️', 'Nada para enviar!')
            return
        
        # No Android, usamos o Kivy Share. No PC, ele apenas copia.
        from kivy.utils import platform
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            String = autoclass('java.lang.String')
            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")
            intent.putExtra(Intent.EXTRA_TEXT, String(self.last_result))
            PythonActivity.mActivity.startActivity(Intent.createChooser(intent, String("Enviar via:")))
        else:
            Clipboard.copy(self.last_result)
            self.show_popup('🖥️ PC', 'Opção "Enviar" copiou o texto (Recurso nativo de Android).')

    def copy_text(self, instance):
        if self.last_result:
            Clipboard.copy(self.last_result)
            self.show_popup('✅', 'Copiado!')

    def clear_fields(self, instance):
        self.msg_input.text = ''
        self.pwd_input.text = ''
        self.result_label.text = 'Aguardando...'
        self.last_result = ""

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.25)).open()

if __name__ == '__main__':
    CryptoGuard().run()
