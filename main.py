from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.agenda import Agenda
from screens.avaliacoes_feitas import AvaliacoesFeitas
from screens.avaliacoes import Avaliacoes
from screens.cadastro import Cadastro
from screens.dentro_do_grupo import DentroDoGrupo
from screens.editar_avaliacoes import EditarAvaliacoes
from screens.editar_grupo import EditarGrupo
from screens.fazer_avaliacoes import FazerAvaliacoes
from screens.grupos import Grupos
from screens.home_screen import HomeScreen
from screens.login import Login
from screens.mensagem_grupo import MensagemGrupo
from screens.meus_grupos import MeusGrupos
from screens.minhas_avaliacoes import MinhasAvaliacoes
from screens.novo_grupo import NovoGrupo

class PowerTrainerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Agenda(name='agenda'))
        sm.add_widget(AvaliacoesFeitas(name='avaliacoes_feitas'))
        sm.add_widget(Avaliacoes(name='avaliacoes'))
        sm.add_widget(Cadastro(name='cadastro'))
        sm.add_widget(DentroDoGrupo(name='dentro_do_grupo')) 
        sm.add_widget(EditarAvaliacoes(name='editar_avaliacoes')) 
        sm.add_widget(EditarGrupo(name='editar_grupo')) 
        sm.add_widget(FazerAvaliacoes(name='fazer_avaliacoes')) 
        sm.add_widget(Grupos(name='grupos'))
        sm.add_widget(HomeScreen(name='home_screen'))
        sm.add_widget(Login(name='login'))  # Adiciona a tela de login
        sm.add_widget(MeusGrupos(name='meus_grupos'))
        sm.add_widget(MensagemGrupo(name='mensagem_grupo'))
        sm.add_widget(MinhasAvaliacoes(name='minhas_avaliacoes'))
        sm.add_widget(NovoGrupo(name='novo_grupo'))
        # Define a tela inicial como login
        sm.current = 'login'
        return sm



if __name__ == '__main__':
    PowerTrainerApp().run()