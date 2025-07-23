from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from database import connect_to_db
import mysql.connector
from kivy.app import App

class MeusGrupos(Screen):
 
    def on_pre_enter(self, *args):
        # Quando a tela é carregada, limpamos o layout e carregamos os grupos
        self.ids.grupo_grid.clear_widgets()
        self.carregar_grupos() 

    def carregar_grupos(self):
        try:

            app = App.get_running_app()
            user_id = app.user_id  # Pegando o ID do usuário que fez login
            
            # Conectando ao banco de dados
            conexao = connect_to_db()  # Chama sua função de conexão
            cursor = conexao.cursor()

            # Executando a consulta SQL para buscar os grupos
            query = """
                   SELECT g.id, g.nome, g.genero, g.limite_membros, g.descricao, e.nome as esporte_nome
                FROM grupo g
                JOIN esporte e ON g.esportes_id = e.id
                JOIN usuario_grupo ug ON g.id = ug.grupo_id
                WHERE ug.usuario_id = %s
                   """
            cursor.execute(query, (user_id,))
            grupos = cursor.fetchall()

            # Para cada grupo retornado, chamamos a função adicionar_grupo
            for grupo in grupos:
                self.adicionar_grupo(grupo)

            # Fechando a conexão com o banco de dados
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar grupos no banco de dados: {erro}")

    def adicionar_grupo(self, grupo):
        # Descompactando os dados do grupo
        id, nome, genero, limite_membros, descricao, esporte_nome = grupo
        
        # Criando um layout para o grupo (por exemplo, um BoxLayout vertical)
        layout = BoxLayout(orientation='horizontal', padding=5, spacing=10, size_hint_y=None, height=60)
          # Ocupar o espaço restante da tela


        # Criando labels para exibir as informações de cada grupo
        imprimirgrupos = Label(text=f" {nome}\n"  # Primeira linha: Nome
                       f"  {genero} | {esporte_nome}\n"  
                       f" {descricao}",
        size_hint_y=None,
        height=layout.height)
        botao_acao = Button(text="Abrir", size_hint_x=None, width=80, height=40, size_hint_y=None)
        botao_acao.bind(on_release=lambda instance: self.abrir_grupo(id))
        # Adicionando os labels ao layout
        layout.add_widget(imprimirgrupos)
        layout.add_widget(botao_acao)

        # Adicionando o layout ao GridLayout da interface
        self.ids.grupo_grid.add_widget(layout)
        layout.height = max(imprimirgrupos.height, botao_acao.height)
    
    def abrir_grupo(self, grupo_id):
     # Aqui você pode redirecionar para a tela do grupo específico
        app = App.get_running_app()
        app.grupo_id_atual = grupo_id  # Armazena o grupo_id no aplicativo
        
        # Redirecionar para a tela do grupo (por exemplo, 'grupo_screen')
        self.manager.current = 'dentro_do_grupo'

    def voltar_home(self):
         self.manager.current = 'home_screen'