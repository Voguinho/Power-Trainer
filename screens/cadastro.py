from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from database import connect_to_db

class Cadastro(Screen):
    def __init__(self, **kwargs):
        super(Cadastro, self).__init__(**kwargs)
        # Inicializações adicionais, se necessárias

    def tirar_foto(self, instance):
        # Implementar lógica para tirar foto
        pass

    def importar_foto(self, instance):
        # Implementar lógica para importar foto
        pass

    def on_cadastrar(self, instance):
        user_data = self.get_user_data()

        if not user_data['termos_aceitos']:
            self.show_popup("Erro", "Você deve aceitar os Termos e Condições.")
            return

        if self.is_email_duplicated(user_data['email']):
            self.show_popup("Erro", "O email já está em uso.")
            return

        if self.save_user_to_db(user_data):
            self.show_popup("Sucesso", "Cadastro realizado com sucesso!")
            self.manager.current = 'login'  # Redireciona para a tela de login
        else:
            self.show_popup("Erro", "Erro ao cadastrar usuário.")

    def go_to_login(self, instance):
        self.manager.current = 'login'  # Redireciona para a tela de login

    def get_user_data(self):
        """Obtém os dados do usuário do formulário."""
        return {
            'nome': self.ids.nome_input.text,
            'email': self.ids.email_input.text,
            'senha': self.ids.senha_input.text,
            'nivel_de_treino': self.ids.nivel_de_treino_input.text,
            'objetivo': self.ids.objetivo_input.text,
            'genero': self.ids.genero_input.text,
            'imagem_perfil': None,  # Será necessário tratar a imagem
            'termos_aceitos': self.ids.termos_checkbox.active,
        }

    def is_email_duplicated(self, email):
        """Verifica se o email já existe no banco de dados."""
        connection = connect_to_db()
        cursor = connection.cursor()
        query = "SELECT * FROM Usuario WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None

    def save_user_to_db(self, user_data):
        """Salva o usuário no banco de dados."""
        try:
            connection = connect_to_db()
            cursor = connection.cursor()

            query = """
                INSERT INTO Usuario (nome, email, senha, nivel_de_treino, objetivo, genero, imagem_perfil)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                user_data['nome'],
                user_data['email'],
                user_data['senha'],
                user_data['nivel_de_treino'],
                user_data['objetivo'],
                user_data['genero'],
                user_data['imagem_perfil']  # Aqui você deve passar o BLOB da imagem, caso tenha sido implementado
            ))

            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar no banco: {e}")
            return False

    def show_popup(self, title, message):
        """Exibe um popup com uma mensagem."""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message)
        popup_button = Button(text="OK", size_hint_y=None, height=50)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.5))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()