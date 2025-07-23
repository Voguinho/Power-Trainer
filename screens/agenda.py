from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import calendar
from datetime import datetime
 
class Agenda(Screen):
    def __init__(self, **kwargs):
        super(Agenda, self).__init__(**kwargs)

        # Layout principal
        layout = BoxLayout(orientation='vertical')

        # Título da tela
        titulo = Label(text='Agenda', font_size='24sp', size_hint_y=None, height=50)
        layout.add_widget(titulo)

        # Widget de Calendário
        self.calendario = CalendarWidget()
        layout.add_widget(self.calendario)

        # Botão de Seleção
        botao_selecionar = Button(text='Selecionar', size_hint_y=None, height=50)
        botao_selecionar.bind(on_press=self.on_selecionar)
        layout.add_widget(botao_selecionar)

        self.add_widget(layout)

    def on_selecionar(self, instance):
        # Função que será chamada quando o botão de "Selecionar" for pressionado
        data_selecionada = self.calendario.get_selected_date()
        print(f'Data Selecionada: {data_selecionada}')
        # Aqui você pode adicionar o código para lidar com a data selecionada


class CalendarWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(CalendarWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        # Header para mostrar o mês e ano e botões de navegação
        header = BoxLayout(size_hint_y=0.1)
        self.month_label = Label(text=self.get_month_year_string())
        prev_button = Button(text='<', on_release=self.show_previous_month)
        next_button = Button(text='>', on_release=self.show_next_month)
        header.add_widget(prev_button)
        header.add_widget(self.month_label)
        header.add_widget(next_button)

        # GridLayout para os dias do mês
        self.days_layout = GridLayout(cols=7)
        self.populate_days()

        self.add_widget(header)
        self.add_widget(self.days_layout)

    def get_month_year_string(self):
        return datetime(self.current_year, self.current_month, 1).strftime('%B %Y')

    def populate_days(self):
        self.days_layout.clear_widgets()
        # Cabeçalho com os dias da semana
        for day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
            self.days_layout.add_widget(Label(text=day))

        # Dias do mês
        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)
        for week in month_calendar:
            for day in week:
                if day == 0:
                    self.days_layout.add_widget(Label(text=''))
                else:
                    self.days_layout.add_widget(Button(text=str(day), on_release=self.on_day_select))

    def on_day_select(self, instance):
        selected_day = instance.text
        selected_date = f"{selected_day}/{self.current_month}/{self.current_year}"
        popup = Popup(title="Selected Date",
                      content=Label(text=f"Você selecionou: {selected_date}"),
                      size_hint=(0.6, 0.4))
        popup.open()

    def show_previous_month(self, instance):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.month_label.text = self.get_month_year_string()
        self.populate_days()

    def show_next_month(self, instance):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.month_label.text = self.get_month_year_string()
        self.populate_days()
# Adicionar esta tela ao seu `ScreenManager` no main.py:
# sm.add_widget(Agenda(name='agenda'))