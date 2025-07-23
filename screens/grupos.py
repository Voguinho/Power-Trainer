from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from database import connect_to_db
import mysql.connector
from kivy.app import App

class Grupos(Screen):

   
    
    def on_pre_enter(self, *args):
        # Quando a tela é carregada, limpamos o layout e carregamos os grupos
        self.ids.grupo_grid.clear_widgets()
        self.carregar_grupos()

    def mostrar_popup(self, titulo, mensagem):
        # Layout do Popup
        box = BoxLayout(orientation='vertical', padding=10)
        box.add_widget(Label(text=mensagem))

        # Botão de fechamento
        botao_fechar = Button(text="Fechar", size_hint_y=None, height=40)
        botao_fechar.bind(on_release=lambda *args: (popup.dismiss(), self.on_pre_enter()))
        box.add_widget(botao_fechar)

        # Criação do Popup
        popup = Popup(title=titulo, content=box, size_hint=(None, None), size=(400, 200))
        popup.open()

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
                  LEFT JOIN usuario_grupo ug ON g.id = ug.grupo_id AND ug.usuario_id = %s
                  WHERE ug.grupo_id IS NULL
                   """
            cursor.execute(query, (user_id,))
            grupos = cursor.fetchone()

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
        botao_acao = Button(text="Entrar", size_hint_x=None, width=80, height=40, size_hint_y=None)
        botao_acao.bind(on_release=lambda instance: (self.entrar_grupo(id), self.mostrar_popup("Sucesso", f"Você entrou no grupo com sucesso")))
        # Adicionando os labels ao layout
        layout.add_widget(imprimirgrupos)
        layout.add_widget(botao_acao)

        # Adicionando o layout ao GridLayout da interface
        self.ids.grupo_grid.add_widget(layout)
        layout.height = max(imprimirgrupos.height, botao_acao.height)

    def entrar_grupo(self, id):
        # Acessa o ID do usuário logado da instância do aplicativo
        app = App.get_running_app()
        user_id = app.user_id  # Pegando o ID do usuário que fez login

        if user_id:
            try:
                # Conectar ao banco de dados
                conexao = connect_to_db()  # Usa a função de conexão ao banco
                cursor = conexao.cursor()

                # Consulta para inserir o relacionamento entre o usuário e o grupo
              
                query = "  INSERT INTO Usuario_Grupo (usuario_id, grupo_id, estrelas, confirmacao, pago, adm) VALUES (%s, %s, 0.0, NULL, NULL, 'N');"
                cursor.execute(query, (user_id, id))

                # Confirma a transação
                conexao.commit()

                # Fechando a conexão com o banco de dados
                cursor.close()
                conexao.close()

                # Confirmação de que o usuário entrou no grupo
                print(f"Usuário com ID {user_id} entrou no grupo com ID: {id}")

            except mysql.connector.Error as erro:
                print(f"Erro ao registrar entrada no grupo: {erro}")

        else:
            print("Erro: Usuário não está logado")
            
    def voltar_home(self):
         self.manager.current = 'home_screen'
    

   