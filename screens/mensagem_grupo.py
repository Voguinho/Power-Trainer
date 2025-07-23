from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from database import connect_to_db
import mysql.connector
from kivy.app import App

class MensagemGrupo(Screen):
    def __init__(self, **kwargs):
        super(MensagemGrupo, self).__init__(**kwargs)
        self.group_id = None  # Vamos usar este ID para carregar o grupo correto

    def on_pre_enter(self, *args):
        # Quando a tela é carregada, limpamos o layout e carregamos as mensagens do grupo
        app = App.get_running_app()
        self.group_id = app.grupo_id_atual  # Acessa o grupo_id armazenado no aplicativo
        self.ids.mensagens_layout.clear_widgets()  # Limpa o layout das mensagens
        self.carregar_mensagens(self.group_id)  # Carrega as mensagens do grupo
        self.definir_nome_grupo(self.group_id)

    def definir_nome_grupo(self, grupo_id):
        # Puxar o nome do grupo do banco de dados
        try:
            conexao = connect_to_db()
            cursor = conexao.cursor()

            query = "SELECT nome FROM grupo WHERE id = %s"
            cursor.execute(query, (grupo_id,))
            nome_grupo = cursor.fetchone()

            if nome_grupo:
                self.ids.nome_grupo.text = nome_grupo[0]

            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar o nome do grupo: {erro}")

    def carregar_mensagens(self, grupo_id):
        try:
            # Conecta ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Consulta para buscar as mensagens do grupo
            query = """
            SELECT m.mensagem, u.nome, m.data_criacao
            FROM mensagem m
            JOIN usuario u ON m.usuario_id = u.id
            WHERE m.grupo_id = %s
            ORDER BY m.data_criacao ASC
        """
            cursor.execute(query, (grupo_id,))
            mensagens = cursor.fetchall()

            # Adiciona cada mensagem na tela de chat
            for mensagem, usuario, data_envio in mensagens:
                self.adicionar_mensagem(f"{usuario}: {mensagem} ({data_envio})")

            # Fecha a conexão com o banco de dados
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar mensagens do chat: {erro}")

    def adicionar_mensagem(self, mensagem):
        # Adiciona uma mensagem ao layout de mensagens
        label = Label(text=mensagem, size_hint_y=None, height=40)
        self.ids.mensagens_layout.add_widget(label)
        self.ids.scroll_view.scroll_y = 0

    def enviar_mensagem(self, instance):
        mensagem = self.ids.text_input.text
        
        if mensagem:
         try:
            app = App.get_running_app()
            usuario_id = app.user_id  # Supondo que o ID do usuário logado seja armazenado no app
            grupo_id = self.group_id  # ID do grupo atual
                # Conecta ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Insere a mensagem no banco de dados
            query = """
                INSERT INTO mensagem (mensagem, usuario_id, grupo_id, data_criacao)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (mensagem, usuario_id, grupo_id))
            conexao.commit()

            # Adiciona a mensagem ao layout do chat
            self.adicionar_mensagem(f"Você: {mensagem}")

            # Limpa o campo de texto após o envio
            self.ids.text_input.text = ''

            # Fecha a conexão
            cursor.close()
            conexao.close()

         except mysql.connector.Error as erro:
            print(f"Erro ao enviar mensagem: {erro}")


    def voltar(self):
        self.manager.current = 'dentro_do_grupo'    