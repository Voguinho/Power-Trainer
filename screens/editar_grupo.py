from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import connect_to_db
import mysql.connector

class EditarGrupo(Screen):
    def __init__(self, **kwargs):
        super(EditarGrupo, self).__init__(**kwargs)
        self.evento_id = None

    def on_pre_enter(self, *args):
        # Carrega os dados do evento antes de entrar na tela
        self.carregar_dados_do_evento()

    def carregar_dados_do_evento(self):
        app = App.get_running_app()
        grupo_id = app.grupo_id_atual  # ID do grupo onde o evento está

        try:
            # Conectar ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Query para buscar os dados do evento existente
            query = """
                SELECT data_hora, local_id, confirmado, limite_jogadores 
                FROM evento 
                WHERE grupo_id = %s
            """
            cursor.execute(query, (grupo_id,))
            self.evento_atual = cursor.fetchone()

            # Fechar cursor e conexão
            cursor.close()
            conexao.close()

            # Verificar se o evento existe
            if self.evento_atual:
                # Preencher os campos de input com os dados do evento
                self.ids.data_hora_input.text = str(self.evento_atual[0])
                self.ids.local_input.text = str(self.evento_atual[1])
                self.ids.confirmado_input.text = str(self.evento_atual[2])
                self.ids.limite_jogadores_input.text = str(self.evento_atual[3])
            else:
                print("Nenhum evento encontrado para o grupo.")

        except mysql.connector.Error as e:
            print(f"Erro ao carregar evento: {e}")
            self.mostrar_popup_erro("Erro ao carregar os dados do evento.")

    def salvar_evento(self):
        app = App.get_running_app()
        grupo_id = app.grupo_id_atual  # ID do grupo onde o evento está

        data_hora = self.ids.data_hora_input.text
        local_id = self.ids.local_input.text
        confirmado = self.ids.confirmado_input.text
        limite_jogadores = self.ids.limite_jogadores_input.text

        if not data_hora or not local_id or not confirmado or not limite_jogadores:
            self.mostrar_popup_erro("Todos os campos devem ser preenchidos.")
            return

        try:
            # Conectar ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Atualizar os dados do evento existente
            query = """
                UPDATE evento 
                SET data_hora = %s, local_id = %s, confirmado = %s, limite_jogadores = %s
                WHERE grupo_id = %s
            """
            cursor.execute(query, (data_hora, local_id, confirmado, limite_jogadores, grupo_id))
            conexao.commit()

            # Fechar cursor e conexão
            cursor.close()
            conexao.close()

            print("Evento atualizado com sucesso!")
            self.manager.current = 'dentro_do_grupo'  # Voltar para a tela anterior

        except mysql.connector.Error as e:
            print(f"Erro ao atualizar evento: {e}")
            self.mostrar_popup_erro("Erro ao salvar as alterações do evento.")

    def mostrar_popup_erro(self, mensagem):
        # Função para exibir uma mensagem de erro
        popup = Popup(title='Erro',
                      content=Label(text=mensagem),
                      size_hint=(None, None), size=(400, 400))
        popup.open()