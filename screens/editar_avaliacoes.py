from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import connect_to_db
import mysql.connector

class EditarAvaliacoes(Screen):
    def __init__(self, **kwargs):
        super(EditarAvaliacoes, self).__init__(**kwargs)
        self.avaliacao_atual = None  # Para armazenar a avaliação que foi carregada
        self.participante_id = None

    def on_pre_enter(self, *args):
        # Carrega a avaliação antes de entrar na tela
        self.carregar_avaliacao()

    def carregar_avaliacao(self):
        app = App.get_running_app()
        usuario_id = app.user_id  # Quem está avaliando
        grupo_id = app.grupo_id_atual  # Grupo no qual a avaliação está ocorrendo
        participante_id = app.participante_id_atual  # Participante sendo avaliado

        try:
            # Conectar ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Query para buscar a avaliação existente
            query = """
                SELECT habilidade, personalidade, comentario 
                FROM avaliacoes 
                WHERE usuario_id = %s AND avaliado_id = %s AND grupo_id = %s
            """
            cursor.execute(query, (usuario_id, participante_id, grupo_id))
            self.avaliacao_atual = cursor.fetchone()

            # Fechar cursor e conexão
            cursor.close()
            conexao.close()

            # Verificar se existe uma avaliação
            if self.avaliacao_atual:
                # Preencher os campos de input com a avaliação atual
                self.ids.habilidade_input.text = str(self.avaliacao_atual[0])
                self.ids.personalidade_input.text = str(self.avaliacao_atual[1])
                self.ids.comentario_input.text = self.avaliacao_atual[2]
            else:
                print("Nenhuma avaliação encontrada.")
                print({usuario_id})
                print({participante_id})
                print({grupo_id})

        except mysql.connector.Error as e:
            print(f"Erro ao carregar avaliação: {e}")
            self.mostrar_popup_erro("Erro ao carregar a avaliação.")

    def enviar_avaliacao(self):
        app = App.get_running_app()
        usuario_id = app.user_id  # Quem está avaliando
        grupo_id = app.grupo_id_atual  # Grupo no qual a avaliação está ocorrendo
        participante_id = app.participante_id_atual  # Participante sendo avaliado

        habilidade = self.ids.habilidade_input.text
        personalidade = self.ids.personalidade_input.text
        comentario = self.ids.comentario_input.text

        if not habilidade or not personalidade or not comentario:
            self.mostrar_popup_erro("Todos os campos devem ser preenchidos.")
            return

        try:
            # Conectar ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Atualizar a avaliação existente
            query = """
                UPDATE avaliacoes 
                SET habilidade = %s, personalidade = %s, comentario = %s
                WHERE usuario_id = %s AND avaliado_id = %s AND grupo_id = %s
            """
            cursor.execute(query, (habilidade, personalidade, comentario, usuario_id, participante_id, grupo_id))
            conexao.commit()

            # Fechar cursor e conexão
            cursor.close()
            conexao.close()

            print("Avaliação atualizada com sucesso!")
            self.manager.current = 'dentro_do_grupo'  # Voltar para a tela anterior

        except mysql.connector.Error as e:
            print(f"Erro ao atualizar avaliação: {e}")
            self.mostrar_popup_erro("Erro ao enviar a avaliação.")

    def mostrar_popup_erro(self, mensagem):
        # Função para exibir uma mensagem de erro
        popup = Popup(title='Erro',
                      content=Label(text=mensagem),
                      size_hint=(None, None), size=(400, 400))
        popup.open()