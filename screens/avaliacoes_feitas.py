from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.app import App
from database import connect_to_db
import mysql.connector

class AvaliacoesFeitas(Screen):
 
    def on_pre_enter(self, *args):
        # Quando a tela é carregada, limpamos o layout e carregamos as avaliações
        self.ids.avaliacao_grid.clear_widgets()
        self.carregar_avaliacoes()
        
    def carregar_avaliacoes(self):
        
        try:
            app = App.get_running_app()
            user_id = app.user_id  # Pegando o ID do usuário que fez login
            
            # Conectando ao banco de dados
            conexao = connect_to_db()  # Chama sua função de conexão
            cursor = conexao.cursor()

            # Executando a consulta SQL para buscar as avaliações feitas pelo usuário
            query = """
                 SELECT a.id, a.habilidade, a.personalidade, a.comentario, g.nome as nome_grupo, u.nome as nome_avaliado, a.grupo_id, a.avaliado_id
            FROM avaliacoes a
            JOIN grupo g ON a.grupo_id = g.id
            JOIN usuario u ON a.avaliado_id = u.id
            WHERE a.usuario_id = %s
            """
            cursor.execute(query, (user_id,))
            avaliacoes = cursor.fetchall()

            # Para cada avaliação retornada, chamamos a função adicionar_avaliacao
            for avaliacao in avaliacoes:
                self.adicionar_avaliacao(avaliacao)

            # Fechando a conexão com o banco de dados
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar avaliações no banco de dados: {erro}")

    def adicionar_avaliacao(self, avaliacao):
     
    # Descompacta os dados da avaliação corretamente
     avaliacao_id, habilidade, personalidade, comentario, nome_grupo, nome_avaliado, grupo_id, avaliado_id = avaliacao
     

    # Cria um BoxLayout para cada avaliação
     layout = BoxLayout(orientation='vertical', size_hint_y=None, height=160, padding=10)

    # Cria labels para mostrar as informações da avaliação
     imprimiravaliacao = Label(text=f" {habilidade}\n"  # Primeira linha: Nome
                       f" {personalidade} | {comentario} | {nome_grupo}\n"  
                       f" {nome_avaliado}",
     size_hint_y=None,
     height=layout.height)
     botao_acao = Button(text="Editar", size_hint_x=None, width=80, height=40, size_hint_y=None)
     botao_acao.bind(on_release=lambda instance: self.editar_avaliacao( grupo_id, avaliado_id))
     
     layout.add_widget(imprimiravaliacao)
     layout.add_widget(botao_acao)

    # Adiciona o layout da avaliação ao GridLayout (avaliacao_grid)
     self.ids.avaliacao_grid.add_widget(layout)

    def editar_avaliacao(self, grupo_id, avaliado_id):
     
     app = App.get_running_app()
     usuario_id = app.user_id    # Quem fez a avaliação (avaliador)
     app.grupo_id_atual = grupo_id  # ID do grupo
     app.participante_id_atual = avaliado_id  # Quem foi avaliado
     
    # Redireciona para a tela de edição
     self.manager.current = 'editar_avaliacoes'

    def voltar_home(self):
        # Lógica para voltar para a tela principal
        self.manager.current = 'home_screen'

    def ir_para_minhas_avaliacoes(self):
        # Lógica para redirecionar para a tela "Minhas Avaliações"
        self.manager.current = 'minhas_avaliacoes'    