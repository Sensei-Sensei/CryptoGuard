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
from kivy.utils import platform

# Configuração de Cores - Paleta Deep Dark
BG_COLOR = (0.05, 0.05, 0.07, 1)
CARD_COLOR = (0.1, 0.1, 0.13, 1)
ACCENT_BLUE = (0.1, 0.5, 0.9, 1)
TEXT_PRIMARY = (0.95, 0.95, 0.95, 1)

Window.clearcolor = BG_COLOR

class CryptoGuard(App):
    def build(self):
        self.title = 'CryptoGuard'
        self.last_result = ""
        
        # Layout Principal
        root = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # HEADER
        header = Label(
            text='[b]CRYPTO[color=#1E88E5]GUARD[/color][/b]',
            markup=True,
            font_size=dp(28),
            size_hint=(1, 0.1),
            color=TEXT_PRIMARY
        )
        root.add_widget(header)
        
        # ÁREA DE INPUT
        self.msg_input = TextInput(
            hint_text='Digite sua mensagem secreta...',
            multiline=True,
            size_hint=(1, 0.25),
            font_size=dp(16),
            background_normal='',
            background_color=CARD_COLOR,
            foreground_color=TEXT_PRIMARY,
            cursor_color=ACCENT_BLUE,
            padding=[dp(15), dp(15)],
            hint_text_color=(0.5, 0.5, 0.6, 1)
        )
        root.add_widget(self.msg_input)
        
        # CAMPO DE SENHA
        self.pwd_input = TextInput(
            hint_text='Chave de Segurança',
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            font_size=dp(16),
            background_normal='',
            background_color=CARD_COLOR,
            foreground_color=TEXT_PRIMARY,
            cursor_color=ACCENT_BLUE,
            padding=[dp(15), dp(13)]
        )
        root.add_widget(self.pwd_input)
        
        # BOTÕES DE AÇÃO
        btn_layout = BoxLayout(size_hint=(1, 0.12), spacing=dp(10))
        
        btn_enc = Button(
            text='CRIPTOGRAFAR',
            background_normal='',
            background_color=ACCENT_BLUE,
            bold=True,
            font_size=dp(14)
        )
        btn_enc.bind(on_press=self.encrypt)
        
        btn_dec = Button(
            text='DESCRIPTOGRAFAR',
            background_normal='',
            background_color=(0.2, 0.23, 0.26, 1),
            bold=True,
            font_size=dp(14)
        )
        btn_dec.bind(on_press=self.decrypt)
        
        btn_layout.add_widget(btn_enc)
        btn_layout.add_widget(btn_dec)
        root.add_widget(btn_layout)
        
        # ÁREA DE RESULTADO (SCROLL)
        result_box = BoxLayout(orientation='vertical', size_hint=(1, 0.22))
        scroll = ScrollView(bar_width=dp(5))
        
        self.result_label = Label(
            text='Aguardando...',
            size_hint_y=None,
            font_size=dp(14),
            color=(0.7, 0.7, 0.7, 1),
            halign='center'
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_label.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))
        
        scroll.add_widget(self.result_label)
        result_box.add_widget(scroll)
        root.add_widget(result_box)

        # BARRA DE UTILITÁRIOS (COM COMPARTILHAMENTO)
        util_box = BoxLayout(size_hint=(1, 0.08), spacing=dp(8))
        
        # Ícones usando caracteres Unicode mais simples para evitar erro de fonte
        utils = [
            ('COPIAR', self.copy_text, (0.2, 0.2, 0.25, 1)),
            ('ENVIAR', self.share_text, (0.13, 0.45, 0.23, 1)),
            ('GERAR', self.generate_password, (0.2, 0.2, 0.25, 1)),
            ('LIMPAR', self.clear_fields, (0.5, 0.15, 0.15, 1))
        ]

        for txt, func, color in utils:
            b = Button(text=txt, background_normal='', background_color=color, font_size=dp(11), bold=True)
            b.bind(on_press=func)
            util_box.add_widget(b)
            
        root.add_widget(util_box)
        return root

    def encrypt(self, instance):
        text = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()
        if not text or not pwd:
            self.show_popup("Aviso", "Preencha texto e senha!")
            return
        
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
            
            encrypted = bytes(a ^ b for a, b in zip(combined, expanded[:len(combined)]))
            hmac = hashlib.sha256(key + encrypted).digest()[:16]
            
            final = base64.b64encode(salt + hmac + encrypted).decode()
            self.result_label.text = f"[Criptografado]\n\n{final}"
            self.last_result = final
        except Exception as e:
            self.show_popup("Erro", str(e))

    def decrypt(self, instance):
        text = self.msg_input.text.strip()
        pwd = self.pwd_input.text.strip()
        try:
            data = base64.b64decode(text)
            salt, hmac_rec, encrypted = data[:16], data[16:32], data[32:]
            key = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt, 100000)
            
            if hashlib.sha256(key + encrypted).digest()[:16] != hmac_rec:
                self.show_popup("Erro", "Senha incorreta!")
                return
                
            expanded = b''
            counter = 0
            while len(expanded) < len(encrypted):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            
            decrypted = bytes(a ^ b for a, b in zip(encrypted, expanded[:len(encrypted)]))
            original = decrypted[8:].decode('utf-8')
            
            self.result_label.text = f"[Mensagem Original]\n\n{original}"
            self.last_result = original
        except:
            self.show_popup("Erro", "Código inválido!")

    def share_text(self, instance):
        if not self.last_result:
            return
        
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                String = autoclass('java.lang.String')
                intent = Intent(Intent.ACTION_SEND)
                intent.setType("text/plain")
                intent.putExtra(Intent.EXTRA_TEXT, String(self.last_result))
                PythonActivity.mActivity.startActivity(Intent.createChooser(intent, String("Enviar via:")))
            except Exception as e:
                self.show_popup("Erro Android", str(e))
        else:
            Clipboard.copy(self.last_result)
            self.show_popup("PC", "Texto copiado!")

    def generate_password(self, instance):
        chars = string.ascii_letters + string.digits
        new_pwd = ''.join(secrets.choice(chars) for _ in range(12))
        self.pwd_input.text = new_pwd
        self.show_popup("Senha Gerada", new_pwd)

    def copy_text(self, instance):
        if self.last_result:
            Clipboard.copy(self.last_result)
            self.show_popup("OK", "Copiado!")

    def clear_fields(self, instance):
        self.msg_input.text = ""
        self.pwd_input.text = ""
        self.result_label.text = "Aguardando..."
        self.last_result = ""

    def show_popup(self, title, message):
        p = Popup(title=title, content=Label(text=message, halign='center'),
                  size_hint=(0.8, 0.25))
        p.open()

if __name__ == '__main__':
    CryptoGuard().run()
