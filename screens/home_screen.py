from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_button_click(self, button_index):
        screen_name = {
            1: 'grupos',
            2: 'agenda',
            3: 'avaliacoes_feitas',
            4: 'meus_grupos',
            5: 'avaliacoes',
            6: 'novo_grupo'
        }.get(button_index)
        if screen_name:
            self.manager.current = screen_name