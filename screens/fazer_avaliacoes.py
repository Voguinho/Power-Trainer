from kivy.uix.screenmanager import Screen
from kivy.app import App
from database import connect_to_db
import mysql.connector

class FazerAvaliacoes(Screen):
    def __init__(self, **kwargs):
        super(FazerAvaliacoes, self).__init__(**kwargs)
        self.group_id = None  # Vamos usar este ID para o grupo
        self.user_id_avaliado = None  # Usaremos este ID para o usuário que será avaliado

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        # Carregar o ID do grupo e do usuário
        self.group_id = app.grupo_id_atual
        self.user_id_avaliado = app.participante_id_atual

        if not self.user_id_avaliado:
            print("Erro ao carregar a avaliação. ID do usuário não encontrado.")
            return

        print(f"ID do participante carregado para avaliação: {self.user_id_avaliado}")
        print(f"ID do grupo carregado para avaliação: {self.group_id}")

        # Limpa os campos de avaliação ao entrar na tela
        self.ids.habilidade_input.text = ''
        self.ids.personalidade_input.text = ''
        self.ids.comentario_input.text = ""

    def enviar_avaliacao(self):
     habilidade = self.ids.habilidade_input.text
     personalidade = self.ids.personalidade_input.text
     comentario = self.ids.comentario_input.text

    # Verificar se os campos não estão vazios
     if not habilidade or not personalidade:
        print("Por favor, insira valores válidos.")
        return

     habilidade = int(habilidade)
     personalidade = int(personalidade)

     app = App.get_running_app()

    # Certificar que o ID do grupo e o ID do usuário avaliado estão presentes
     if not self.group_id:
        print("Erro: ID do grupo não encontrado.")
        return

     if not self.user_id_avaliado:
        print("Erro: ID do usuário avaliado não encontrado.")
        return

    # ID de quem está avaliando
     usuario_id = app.user_id  # Usuário logado (quem está avaliando)
    # ID de quem está sendo avaliado
     avaliado_id = self.user_id_avaliado

     print(f"ID do grupo: {self.group_id}")
     print(f"ID do usuário avaliador: {usuario_id}")
     print(f"ID do usuário avaliado: {avaliado_id}")

     if 1 <= habilidade <= 5 and 1 <= personalidade <= 5:
        try:
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Query de INSERT
            query = """
                INSERT INTO avaliacoes (habilidade, personalidade, comentario, usuario_id, avaliado_id, grupo_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    habilidade = VALUES(habilidade),
                    personalidade = VALUES(personalidade),
                    comentario = VALUES(comentario)
            """

            # Executar a query com os valores corretos
            cursor.execute(query, (
                habilidade, personalidade, comentario, usuario_id, avaliado_id, self.group_id
            ))

            conexao.commit()
            cursor.close()
            conexao.close()

            print("Avaliação enviada com sucesso!")
            self.manager.current = 'dentro_do_grupo'

        except mysql.connector.Error as e:
            print(f"Erro ao enviar avaliação: {e}")
     else:
        print("As avaliações devem ser de 1 a 5.")