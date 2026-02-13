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

class CryptoGuard(App):
    def build(self):
        self.title = '🔐 CryptoGuard'
        
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # TÍTULO
        titulo = Label(
            text='[b][color=#2196F3]🔐 CRYPTO GUARD[/color][/b]',
            markup=True,
            font_size=dp(28),
            size_hint=(1, 0.1)
        )
        layout.add_widget(titulo)
        
        # ÁREA DE MENSAGEM
        self.msg_input = TextInput(
            hint_text='Digite sua mensagem aqui...',
            multiline=True,
            size_hint=(1, 0.25),
            font_size=dp(16)
        )
        layout.add_widget(self.msg_input)
        
        # CAMPO DE SENHA
        self.pwd_input = TextInput(
            hint_text='Digite sua senha',
            password=True,
            multiline=False,
            size_hint=(1, 0.08),
            font_size=dp(16)
        )
        layout.add_widget(self.pwd_input)
        
        # BOTÕES PRINCIPAIS
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=dp(10))
        
        btn_encrypt = Button(
            text='🔒 CRIPTOGRAFAR',
            background_color=(0.13, 0.59, 0.95, 1),
            font_size=dp(16),
            bold=True
        )
        btn_encrypt.bind(on_press=self.encrypt)
        btn_layout.add_widget(btn_encrypt)
        
        btn_decrypt = Button(
            text='🔓 DESCRIPTOGRAFAR',
            background_color=(0.33, 0.33, 0.95, 1),
            font_size=dp(16),
            bold=True
        )
        btn_decrypt.bind(on_press=self.decrypt)
        btn_layout.add_widget(btn_decrypt)
        
        layout.add_widget(btn_layout)
        
        # BOTÕES SECUNDÁRIOS
        btn_layout2 = BoxLayout(size_hint=(1, 0.12), spacing=dp(10))
        
        btn_generate = Button(
            text='🔑 GERAR SENHA',
            background_color=(0.5, 0.5, 0.5, 1),
            font_size=dp(14)
        )
        btn_generate.bind(on_press=self.generate_password)
        btn_layout2.add_widget(btn_generate)
        
        btn_clear = Button(
            text='🧹 LIMPAR',
            background_color=(0.8, 0.3, 0.3, 1),
            font_size=dp(14)
        )
        btn_clear.bind(on_press=self.clear_fields)
        btn_layout2.add_widget(btn_clear)
        
        layout.add_widget(btn_layout2)
        
        # ÁREA DE RESULTADO (COM SCROLL)
        self.result_label = Label(
            text='Resultado aparecerá aqui...',
            size_hint=(1, None),
            height=dp(120),
            font_size=dp(14),
            halign='left',
            valign='top',
            text_size=(None, None),
            color=(0.9, 0.9, 0.9, 1)
        )
        
        scroll = ScrollView(
            size_hint=(1, 0.2),
            bar_width=dp(5),
            bar_color=(0.3, 0.6, 0.9, 1)
        )
        scroll.add_widget(self.result_label)
        layout.add_widget(scroll)
        
        # BOTÃO COPIAR
        btn_copy = Button(
            text='📋 COPIAR RESULTADO',
            size_hint=(1, 0.08),
            background_color=(0.3, 0.7, 0.3, 1),
            font_size=dp(14)
        )
        btn_copy.bind(on_press=self.copy_text)
        layout.add_widget(btn_copy)
        
        return layout
    
    def encrypt(self, instance):
        text = self.msg_input.text.strip()
        password = self.pwd_input.text.strip()
        
        if not text or not password:
            self.show_popup('Erro', 'Preencha todos os campos!')
            return
        
        try:
            # Salt aleatório
            salt = secrets.token_bytes(16)
            
            # Derivar chave com PBKDF2
            key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            
            # Nonce + dados
            nonce = secrets.token_bytes(8)
            data = text.encode()
            combined = nonce + data
            
            # Expandir chave
            expanded = b''
            counter = 0
            while len(expanded) < len(combined):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            expanded = expanded[:len(combined)]
            
            # XOR
            encrypted = bytes(a ^ b for a, b in zip(combined, expanded))
            
            # HMAC para verificação
            hmac = hashlib.sha256(key + encrypted).digest()[:16]
            
            # Combinar tudo
            result = salt + hmac + encrypted
            b64_result = base64.b64encode(result).decode()
            
            self.result_label.text = f'[b]✅ CRIPTOGRAFADO:[/b]\n\n{b64_result}'
            self.result_label.markup = True
            self.last_result = b64_result
            
        except Exception as e:
            self.show_popup('Erro', f'Falha na criptografia: {str(e)}')
    
    def decrypt(self, instance):
        text = self.msg_input.text.strip()
        password = self.pwd_input.text.strip()
        
        if not text or not password:
            self.show_popup('Erro', 'Preencha todos os campos!')
            return
        
        try:
            # Decodificar base64
            data = base64.b64decode(text)
            
            # Extrair componentes
            salt = data[:16]
            hmac_received = data[16:32]
            encrypted = data[32:]
            
            # Derivar chave
            key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            
            # Verificar HMAC
            hmac_calc = hashlib.sha256(key + encrypted).digest()[:16]
            if hmac_received != hmac_calc:
                raise ValueError('Senha incorreta ou mensagem corrompida!')
            
            # Expandir chave
            expanded = b''
            counter = 0
            while len(expanded) < len(encrypted):
                expanded += hashlib.sha256(key + counter.to_bytes(4, 'big')).digest()
                counter += 1
            expanded = expanded[:len(encrypted)]
            
            # XOR
            decrypted = bytes(a ^ b for a, b in zip(encrypted, expanded))
            
            # Remover nonce
            original = decrypted[8:].decode()
            
            self.result_label.text = f'[b]✅ DESCRIPTOGRAFADO:[/b]\n\n{original}'
            self.result_label.markup = True
            self.last_result = original
            
        except ValueError as e:
            self.show_popup('Erro', str(e))
        except Exception as e:
            self.show_popup('Erro', f'Falha na descriptografia: {str(e)}')
    
    def generate_password(self, instance):
        chars = string.ascii_letters + string.digits + '!@#$%&*'
        password = ''.join(secrets.choice(chars) for _ in range(16))
        self.pwd_input.text = password
        self.result_label.text = f'[b]🔑 SENHA GERADA:[/b]\n\n{password}'
        self.result_label.markup = True
        self.last_result = password
        Clipboard.copy(password)
        self.show_popup('Sucesso', 'Senha copiada para área de transferência!')
    
    def clear_fields(self, instance):
        self.msg_input.text = ''
        self.pwd_input.text = ''
        self.result_label.text = 'Resultado aparecerá aqui...'
        self.result_label.markup = False
        self.last_result = None
    
    def copy_text(self, instance):
        if hasattr(self, 'last_result') and self.last_result:
            Clipboard.copy(self.last_result)
            self.show_popup('Sucesso', 'Copiado para área de transferência!')
        else:
            self.show_popup('Aviso', 'Nada para copiar!')
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, font_size=dp(14)),
            size_hint=(0.8, 0.4),
            separator_color=(0.2, 0.6, 0.9, 1)
        )
        popup.open()

if __name__ == '__main__':
    CryptoGuard().run()
