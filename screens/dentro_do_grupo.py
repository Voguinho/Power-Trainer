from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from database import connect_to_db
import mysql.connector
from kivy.app import App
from mysql.connector import Error

class DentroDoGrupo(Screen):
    def __init__(self, **kwargs):
        super(DentroDoGrupo, self).__init__(**kwargs)
        self.group_id = None  # Vamos usar este ID para carregar o grupo correto

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.group_id = app.grupo_id_atual
        print({self.group_id})
        # Limpa os widgets antes de adicionar os novos dados
        self.ids.participantes_layout.clear_widgets()
        self.buscar_dados_grupo()
        self.buscar_participantes()

    def buscar_dados_grupo(self):
        try:
            app = App.get_running_app()
            group_id = app.grupo_id_atual  # Pegando o ID do grupo
            
            # Conectando ao banco de dados
            conexao = connect_to_db()  # Chama sua função de conexão
            cursor = conexao.cursor()

            # Executando a consulta SQL para buscar os dados do grupo
            query = """
                SELECT g.nome, g.genero, g.limite_membros, g.descricao,  
       l.nome AS local, e.nome AS esporte, ev.data_hora, ev.confirmado, ev.limite_jogadores
FROM grupo g
LEFT JOIN evento ev ON g.id = ev.grupo_id
LEFT JOIN local l ON ev.local_id = l.id
LEFT JOIN esporte e ON g.esportes_id = e.id
WHERE g.id = %s;
            """
            cursor.execute(query, (group_id,))
            grupo = cursor.fetchone()

            if grupo:
                # Passa os dados do grupo para serem exibidos
                self.adicionar_dadosdogrupo(grupo)

            # Fechando a conexão com o banco de dados
            cursor.close()
            conexao.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao buscar dados do grupo: {erro}")

    def adicionar_dadosdogrupo(self, grupo):
        # Descompactando os dados do grupo
        nome, genero, limite_membros, descricao,  esporte_nome, data_hora, local, confirmado,limite_pelada, = grupo

    # Atualizando a interface com os dados do grupo
        self.ids.nome_grupo.text = nome
        self.ids.info_grupo.text = f"{genero} - Membros: {limite_membros} - Limite de peladas: {limite_pelada}\n"
        f"{esporte_nome} - Data: {data_hora} - Local: {local} "
        self.ids.descricao_grupo.text = descricao
        
        
        # Atualizando a interface com os dados do grupo   

    def buscar_participantes(self):
        try:
            conexao = connect_to_db()
            cursor = conexao.cursor()
            query_participantes = """
            SELECT u.nome, ug.confirmacao, ug.pago, u.id
            FROM usuario_grupo ug
            JOIN usuario u ON u.id = ug.usuario_id
            WHERE ug.grupo_id = %s
        """
            cursor.execute(query_participantes, (self.group_id,))
            participantes = cursor.fetchall()

            for participante in participantes:
             self.adicionar_participantes(participante)
            # Adicionar o ID do participante à lista

            # Fechando a conexão com o banco de dados
             
            cursor.close()
            conexao.close()

            return participantes
        except mysql.connector.Error as e:
            print(f"Erro ao buscar participantes: {e}")
            return None

    def adicionar_participantes(self, participante):
       nome, confirmacao, pago, participante_id = participante

       layout = BoxLayout(orientation='horizontal', padding=5, spacing=10, size_hint_y=None, height=60)


           # Criando labels para exibir as informações de cada grupo       
       imprimirgrupos = Label(text=f" {nome}\n"  # Primeira linha: Nome
                       f" {confirmacao} | {pago} \n"  ,
        size_hint_y=None,
        height=layout.height)
       botao_acao = Button(text="Pagou", size_hint_x=None, width=80, height=40, size_hint_y=None)
       botao_acao.bind(on_release=lambda instance: self.participante_pagou(participante_id)),
       botao_confirmar = Button(text="Confirmar", size_hint_x=None, width=80, height=40, size_hint_y=None)
       botao_confirmar.bind(on_release=lambda instance: self.confirmar_participantes(participante_id)),
       botao_avaliar = Button(text="Avaliar", size_hint_x=None, width=80, height=40, size_hint_y=None)
       botao_avaliar.bind(on_release=lambda instance: self.avaliar_participante(participante_id))
        # Adicionando os labels ao layout
       layout.add_widget(imprimirgrupos)
       layout.add_widget(botao_acao)
       layout.add_widget(botao_confirmar)
       layout.add_widget(botao_avaliar)
       

        # Adicionando o layout ao GridLayout da interface
       self.ids.participantes_layout.add_widget(layout)
       layout.height = max(imprimirgrupos.height, botao_acao.height,botao_confirmar.height, botao_avaliar.height)

    def participante_pagou(self, participante_id):
          print(f"Participante pagou, ainda tem que fazer")

    def avaliar_participante(self, participante_id):
   
     app = App.get_running_app()
     usuario_id = app.user_id  # Usuário logado (quem está avaliando)
     grupo_id = app.grupo_id_atual  # Grupo onde o usuário está
     app.participante_id_atual = participante_id  

     try:
        # Conectar ao banco de dados
        conexao = connect_to_db()
        cursor = conexao.cursor()

        # Recuperar o user_id e grupo_id a partir do app (sem precisar reinstanciar)
        
        # Query para verificar se a avaliação já existe
        query = """
            SELECT habilidade, personalidade, comentario 
            FROM avaliacoes 
            WHERE usuario_id = %s AND avaliado_id = %s AND grupo_id = %s
        """
        cursor.execute(query, (usuario_id, participante_id, grupo_id))
        avaliacao = cursor.fetchone()

        cursor.close()
        conexao.close()

        if avaliacao:
            # Se já existe uma avaliação, redireciona para a página de edição
            self.manager.current = 'editar_avaliacoes'
        else:
            # Se não existe avaliação, redireciona para a página de nova avaliação
            self.manager.current = 'fazer_avaliacoes'

     except mysql.connector.Error as e:
        print(f"Erro ao verificar avaliação: {e}")
        self.mostrar_popup_erro("Erro ao verificar a avaliação.")

    def abrir_chat(self):
     app = App.get_running_app()
     grupo_id = app.grupo_id_atual  # Acessa o grupo_id armazenado no aplicativo
        # Aqui você pode fazer o que for necessário com o grupo_id
     self.manager.current = 'mensagem_grupo'  # Direciona para a tela de chat       
                          
    def sair_grupo(self):
     try:
        # Pegando o ID do grupo e do usuário atual
       app = App.get_running_app()
       user_id = app.user_id  # ID do usuário logado
       group_id = self.group_id  # ID do grupo atual
        
        # Conectando ao banco de dados
       conexao = connect_to_db()
       cursor = conexao.cursor()

        # Query para remover o usuário do grupo
       query = """
            DELETE FROM usuario_grupo
            WHERE usuario_id = %s AND grupo_id = %s
        """
        
        # Executando a query
       cursor.execute(query, (user_id, group_id))
        
        # Confirmando a operação
       conexao.commit()
        
        # Mensagem de sucesso
       print("Usuário removido com sucesso do grupo.")
        
        # Redirecionar o usuário de volta à lista de grupos, por exemplo
       self.manager.current = 'meus_grupos'  # Ajuste para a tela correta
        
        # Fechando conexão
       cursor.close()
       conexao.close()
     except mysql.connector.Error as erro:
       print(f"Erro ao tentar sair do grupo: {erro}")  # Lógica para sair do grupo (excluir relação no banco de dados)

    def voltar(self):
         self.manager.current = 'meus_grupos'  

    def EditarGrupo(self):
     app = App.get_running_app()
     grupo_id = app.grupo_id_atual  # Grupo onde o usuário está  
     self.manager.current = 'editar_grupo'  

    def confirmar_evento(self):
    
     app = App.get_running_app()
     grupo_id = app.grupo_id_atual
    
     try:
        # Conecta ao banco de dados
        conexao = connect_to_db()
        cursor = conexao.cursor()
        
        # Busca o evento para o grupo (assumindo que só há um evento por grupo)
        query_evento = "SELECT id, data_hora, grupo_id, limite_jogadores, local_id FROM evento WHERE grupo_id = %s"
        cursor.execute(query_evento, (grupo_id,))
        evento = cursor.fetchone()
        
        if evento:
            evento_id = evento[0]
            
            # Confirma o evento
            cursor.execute("UPDATE evento SET confirmado = 1 WHERE id = %s", (evento_id,))
            conexao.commit()
            
            print(f"Evento {evento_id} confirmado.")
            
            # Insere o evento no calendário
            query_calendario = """
            INSERT INTO calendario (grupo_id, data_hora, limite_jogadores, local_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_calendario, (grupo_id, evento[1], evento[3], evento[4]))
            conexao.commit()
            
            # Obtém o ID do novo registro no calendário
            calendario_id = cursor.lastrowid
            
            # Busca os IDs de usuario_grupo confirmados para o grupo
            query_usuarios = "SELECT id FROM usuario_grupo WHERE grupo_id = %s AND confirmacao = 1"
            cursor.execute(query_usuarios, (grupo_id,))
            usuarios_confirmados = cursor.fetchall()
            
            # Registra a participação de cada usuário confirmado no calendário_participante
            for usuario_grupo in usuarios_confirmados:
                usuario_grupo_id = usuario_grupo[0]
                self.registrar_participacao_usuario(calendario_id, usuario_grupo_id)
        
        # Fecha o cursor e a conexão
        cursor.close()
        conexao.close()
        
     except Exception as e:
        print(f"Erro ao confirmar evento: {e}")

    def registrar_participacao_usuario(self, calendario_id, usuario_grupo_id):
    
     try:
        conexao = connect_to_db()
        cursor = conexao.cursor()
        
        # Insere a participação no calendário_participante
        query = """
        INSERT INTO calendario_participante (calendario_id, usuario_grupo_id)
        VALUES (%s, %s)
        """
        cursor.execute(query, (calendario_id, usuario_grupo_id))
        conexao.commit()
        
        # Fecha o cursor e a conexão
        cursor.close()
        conexao.close()
        
        print(f"Participação do usuário_grupo {usuario_grupo_id} no calendário {calendario_id} registrada com sucesso.")
     except Exception as e:
        print(f"Erro ao registrar participação do usuário: {e}")

    def confirmar_participantes(self, usuario_grupo_id):
     try:
        # Obter o grupo_id diretamente do aplicativo
        app = App.get_running_app()
        grupo_id = app.grupo_id_atual

        conexao = connect_to_db()
        cursor = conexao.cursor()

        # Verificar se o evento do grupo está confirmado e obter o último calendário
        query_evento = """
        SELECT e.confirmado, c.id AS calendario_id
        FROM evento e
        LEFT JOIN calendario c ON c.grupo_id = e.grupo_id
        WHERE e.grupo_id = %s
        ORDER BY c.id DESC
        LIMIT 1
        """
        cursor.execute(query_evento, (grupo_id,))
        resultado = cursor.fetchone()

        if not resultado:
            raise Exception("Evento ou calendário não encontrado para o grupo.")

        evento_confirmado, calendario_id = resultado

        if not evento_confirmado:  # Evento NÃO está confirmado
            # Atualizar o status de confirmação no usuario_grupo
            query_atualizar = """
            UPDATE usuario_grupo
            SET confirmacao = 1
            WHERE id = %s
            """
            cursor.execute(query_atualizar, (usuario_grupo_id,))
            conexao.commit()
            print(f"Participante {usuario_grupo_id} marcado como confirmado no grupo {grupo_id}.")
        else:  # Evento está confirmado
            # Registrar a participação no calendário
            self.registrar_participacao_usuario(calendario_id, usuario_grupo_id)
            print(f"Participante {usuario_grupo_id} registrado diretamente no evento confirmado {calendario_id}.")
        
        cursor.close()
        conexao.close()

     except Exception as e:
        print(f"Erro ao confirmar participante: {e}")

