from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from database import connect_to_db
import mysql.connector

class Avaliacoes(Screen):

    def on_pre_enter(self, *args):
        # Limpa o layout e carrega as avaliações recebidas
        self.ids.avaliacao_recebida_grid.clear_widgets()
        self.carregar_avaliacoes_recebidas()
        self.carregar_media_esporte()
        self.carregar_media()  

    def carregar_avaliacoes_recebidas(self):
        try:
            app = App.get_running_app()
            user_id = app.user_id  # Pegando o ID do usuário logado
            
            # Conectando ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Consulta SQL para buscar todas as avaliações recebidas pelo usuário, agrupadas por grupo
            query = """
                SELECT g.nome AS nome_grupo, 
                       AVG(a.habilidade) AS media_habilidade, 
                       AVG(a.personalidade) AS media_personalidade, 
                       COUNT(a.id) AS total_avaliacoes
                FROM avaliacoes a
                JOIN grupo g ON a.grupo_id = g.id
                WHERE a.avaliado_id = %s
                GROUP BY a.grupo_id
            """
            cursor.execute(query, (user_id,))
            avaliacoes_recebidas = cursor.fetchall()

            # Para cada grupo, exibir as médias
            for avaliacao in avaliacoes_recebidas:
                self.adicionar_avaliacao_recebida(avaliacao)

            # Fecha a conexão
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar avaliações no banco de dados: {erro}")

    def adicionar_avaliacao_recebida(self, avaliacao):
        # Descompacta os dados
        nome_grupo, media_habilidade, media_personalidade, total_avaliacoes = avaliacao

        # Cria um layout para exibir a avaliação
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=10)

        # Exibe os dados
        label = Label(text=f"[Grupo: {nome_grupo}] - "
                           f"Média Habilidade: {media_habilidade:.2f}, "
                           f"Média Personalidade: {media_personalidade:.2f} "
                           f"({total_avaliacoes} avaliações)",
                      size_hint_y=None, height=layout.height)
        
        layout.add_widget(label)

        # Adiciona o layout da avaliação ao GridLayout
        self.ids.avaliacao_recebida_grid.add_widget(layout)
   
    def carregar_media_esporte(self):
        try:
            app = App.get_running_app()
            user_id = app.user_id  # Pegando o ID do usuário logado
            
            # Conectando ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Consulta SQL para buscar todas as avaliações recebidas pelo usuário, agrupadas por grupo
            query = """
                SELECT e.nome AS nome_esporte, 
               AVG(a.habilidade) AS media_habilidade, 
               AVG(a.personalidade) AS media_personalidade, 
               COUNT(a.id) AS total_avaliacoes
        FROM avaliacoes a
        JOIN grupo g ON a.grupo_id = g.id
        JOIN esporte e ON g.esportes_id = e.id
        WHERE a.avaliado_id = %s
        GROUP BY e.id
     """
            cursor.execute(query, (user_id,))
            avaliacoes_recebidas = cursor.fetchall()

            # Para cada grupo, exibir as médias
            for avaliacao in avaliacoes_recebidas:
                self.adicionar_media_esporte(avaliacao)

            # Fecha a conexão
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar avaliações no banco de dados: {erro}")

    def adicionar_media_esporte(self, avaliacao):
        # Descompacta os dados
        nome_grupo, media_habilidade, media_personalidade, total_avaliacoes = avaliacao

        # Cria um layout para exibir a avaliação
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=10)

        # Exibe os dados
        label = Label(text=f"[Grupo: {nome_grupo}] - "
                           f"Média Habilidade: {media_habilidade:.2f}, "
                           f"Média Personalidade: {media_personalidade:.2f} "
                           f"({total_avaliacoes} avaliações)",
                      size_hint_y=None, height=layout.height)
        
        layout.add_widget(label)

        # Adiciona o layout da avaliação ao GridLayout
        self.ids.avaliacao_recebida_grid.add_widget(layout)

    def carregar_media(self):
        try:
            app = App.get_running_app()
            user_id = app.user_id  # Pegando o ID do usuário logado
            
            # Conectando ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Consulta SQL para buscar todas as avaliações recebidas pelo usuário, agrupadas por grupo
            query = """
                SELECT AVG(a.habilidade) AS media_habilidade, 
                   AVG(a.personalidade) AS media_personalidade, 
                   COUNT(a.id) AS total_avaliacoes
            FROM avaliacoes a
            WHERE a.avaliado_id = %s
                  """

            cursor.execute(query, (user_id,))
            avaliacoes_recebidas = cursor.fetchall()

            # Para cada grupo, exibir as médias
            for avaliacao in avaliacoes_recebidas:
                self.adicionar_media(avaliacao)

            # Fecha a conexão
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar avaliações no banco de dados: {erro}")

    def adicionar_media(self, avaliacao):
        # Descompacta os dados
        media_habilidade, media_personalidade, total_avaliacoes = avaliacao

        # Cria um layout para exibir a avaliação
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120, padding=10)

        # Exibe os dados
        label = Label(
            text=f"Média Geral - "
                 f"Média Habilidade: {media_habilidade:.2f}, "
                 f"Média Personalidade: {media_personalidade:.2f} "
                 f"({total_avaliacoes} avaliações)",
            size_hint_y=None, height=40  # Altura ajustada diretamente
        )
        
        layout.add_widget(label)

        # Adiciona o layout da avaliação ao GridLayout
        self.ids.avaliacao_recebida_grid.add_widget(layout)

    def voltar_home(self):
        # Lógica para voltar para a tela principal
        self.manager.current = 'home_screen'

    def ir_para_avaliacoes_feitas(self):
        # Lógica para ir para a tela de avaliações feitas
        self.manager.current = 'avaliacoes_feitas'