from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from widgets import Board


class PuzzleGame(PageLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_game()

    def _init_game(self):
        # self.board = AnchorLayout(anchor_x='center', anchor_y='center')
        self.board = Board(self)#, size_hint=(None, None), size=(int(350), int(350)))
        # self.board.add_widget(board)
        self.add_widget(self.board)
        self.help = TextInput(background_color=(0,0,0,1), foreground_color=(1,0,0,1))
        self.add_widget(self.help)

    def on_win(self):
        self.remove_widget(self.board)
        self.remove_widget(self.help)

        self._init_game()



class PuzzleApp(App):
    def build(self):
        return PuzzleGame()


if __name__ == '__main__':
    PuzzleApp().run()