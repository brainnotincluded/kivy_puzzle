from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.pagelayout import PageLayout
from kivy.uix.textinput import TextInput
from widgets import Board


class PuzzleGame(PageLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        board = AnchorLayout(anchor_x='center', anchor_y='center')
        board.add_widget(Board(size_hint=(None, None), size=(350,350)))
        self.add_widget(board)
        self.add_widget(TextInput(background_color=(0,0,0,1), foreground_color=(1,0,0,1)))

class PuzzleApp(App):
    def build(self):
        return PuzzleGame()


if __name__ == '__main__':
    PuzzleApp().run()