from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

class NovoGrupo(Screen):

    def criar_grupo(self):
        """Função para criar o grupo e salvar no banco de dados."""
        # Capturando os valores dos campos
        atividade = self.ids.spinner_atividade.text
        cidade = self.ids.spinner_cidade.text
        data = self.ids.data_input.text  # Capturando a data no formato DD/MM/AAAA
        horario = self.ids.horario_input.text  # Capturando o horário no formato HH:MM
        nivel = self.ids.spinner_nivel.text

        # Verifica se todos os campos estão preenchidos
        if atividade == "Escolher" or cidade == "Escolher" or data == "" or horario == "" or nivel == "Escolher":
            popup = Popup(title='Erro',
                          content=Label(text='Preencha todos os campos!'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            # Aqui você pode conectar ao banco de dados para salvar o grupo
            print(f"Criando grupo: {atividade}, {cidade}, {data}, {horario}, {nivel}")

            # Exemplo de popup para confirmar o sucesso da criação do grupo
            popup = Popup(title='Sucesso',
                          content=Label(text='Grupo criado com sucesso!'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

            # Voltar para a tela de grupos após criar o grupo
            self.manager.current = 'grupos'
