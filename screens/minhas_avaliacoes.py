from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from database import connect_to_db
import mysql.connector

class MinhasAvaliacoes(Screen):
    
    def on_pre_enter(self, *args):
        # Limpa o layout quando a tela é carregada e carrega as avaliações
        self.ids.avaliacao_grid.clear_widgets()
        self.carregar_avaliacoes_recebidas()

    def carregar_avaliacoes_recebidas(self):
        try:
            app = App.get_running_app()
            user_id = app.user_id  # Pegando o ID do usuário logado (avaliado)
            
            # Conectando ao banco de dados
            conexao = connect_to_db()
            cursor = conexao.cursor()

            # Consulta SQL para buscar as avaliações recebidas pelo usuário logado
            query = """
                SELECT a.habilidade, a.personalidade, a.comentario, g.nome AS nome_grupo, u.nome AS nome_avaliador, a.grupo_id, a.usuario_id
                FROM avaliacoes a
                JOIN grupo g ON a.grupo_id = g.id
                JOIN usuario u ON a.usuario_id = u.id
                WHERE a.avaliado_id = %s
            """
            cursor.execute(query, (user_id,))
            avaliacoes = cursor.fetchall()

            # Para cada avaliação recebida, adicionamos à tela
            for avaliacao in avaliacoes:
                self.adicionar_avaliacao(avaliacao)

            # Fechando a conexão com o banco de dados
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar avaliações recebidas: {erro}")

    def adicionar_avaliacao(self, avaliacao):

        # Descompacta os dados da avaliação recebida
        habilidade, personalidade, comentario, nome_grupo, nome_avaliador, grupo_id, usuario_id = avaliacao

        # Cria um layout para exibir as informações da avaliação
        layout = BoxLayout(orientation='vertical', size_hint_y=None, height=160, padding=10)

        # Cria labels para mostrar as informações da avaliação
        imprimir_avaliacao = Label(text=f"Avaliador: {nome_avaliador}\n"
                                        f"Habilidade: {habilidade}\n"
                                        f"Personalidade: {personalidade}\n"
                                        f"Comentário: {comentario}\n"
                                        f"Grupo: {nome_grupo}",
                                   size_hint_y=None, height=layout.height)

        layout.add_widget(imprimir_avaliacao)

        # Adiciona o layout da avaliação ao GridLayout (avaliacao_grid)
        self.ids.avaliacao_grid.add_widget(layout)

    def voltar(self):
        self.manager.current = 'home_screen'   

    def ir_para_avaliacoes_feitas(self):
        self.manager.current = 'avaliacoes_feitas'   