from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from widgets import Board, Win


class PuzzleGame(PageLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_game()

    def _init_game(self):
        # self.board = AnchorLayout(anchor_x='center', anchor_y='center')
        self.board = Board(self)  # , size_hint=(None, None), size=(int(350), int(350)))
        # self.board.add_widget(board)
        self.add_widget(self.board)
        self.help = TextInput(
            readonly=True,
            cursor_color=(0, 0, 0, 0),
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 0, 0, 1),
            text=self.board.room.say())

        self.add_widget(self.help)


    def on_win(self):
        self.add_widget(Win(self, [self.board, self.help]))




class PuzzleApp(App):

    def build(self):
        # Window.size = (300, 550)
        return PuzzleGame()


if __name__ == '__main__':
    PuzzleApp().run()
