from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label
from database import connect_to_db


class Login(Screen):
    def on_login(self, instance):
        email = self.ids.user_input.text
        password = self.ids.password_input.text

        if self.verify_login(email, password):
            App.get_running_app().user_id = self.user_id
            self.manager.current = 'home_screen'
        else:
            # Remove mensagens de erro anteriores, se houver
            for widget in self.children[:]:
                if isinstance(widget, Label) and widget.text.startswith("Email ou senha inválidos!"):
                    self.remove_widget(widget)
            
            # Exibe a mensagem de erro
            error_label = Label(text="Email ou senha inválidos!", color=(1, 0, 0, 1), font_size=16)
            self.add_widget(error_label)

    def on_register(self, instance):
        self.manager.current = 'cadastro'  # Redireciona para a tela de cadastro

    def verify_login(self, email, password):
        connection = connect_to_db()  # Usa a função connect_to_db da página database.py
        cursor = connection.cursor()
        query = "SELECT id FROM Usuario WHERE email = %s AND senha = %s"  # Obtendo o ID
        cursor.execute(query, (email, password))
        result = cursor.fetchone()

        if result:  # Se a consulta retornar um resultado válido
            self.user_id = result[0]  # O ID do usuário está na primeira coluna
        else:
            self.user_id = None  # Login inválido, nenhum ID será armazenado

        cursor.close()
        connection.close()

        return result