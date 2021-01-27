from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.pagelayout import PageLayout
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from widgets import Board, Win, Pause, Volume, Candle


class Settings(BoxLayout):
    def __init__(self, music, **kwargs):
        super().__init__(**kwargs)

        self.music = music

        self.orientation = 'vertical'

        # Add top: volume control
        self.add_widget(Volume(self.music))

        self.hor_boxes = BoxLayout(orientation='horizontal')
        # Add bottom: 3 horizontal boxes
        self.add_widget(self.hor_boxes)

        self.anc1 = AnchorLayout(anchor_x='left', anchor_y='bottom')
        self.anc2 = AnchorLayout()
        self.anc3 = AnchorLayout(anchor_x='right', anchor_y='bottom')

        self.hor_boxes.add_widget(self.anc1)
        self.hor_boxes.add_widget(self.anc2)
        self.hor_boxes.add_widget(self.anc3)

        self.anc1.add_widget(Candle())
        self.anc3.add_widget(Candle())


class PuzzleGame(PageLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.to_close = []
        self.music = SoundLoader.load('sound/music.wav')
        self.music.loop = True
        self.music.volume = 1
        if self.music:
            self.music.play()
        self._init_game()

    def add_to_close(self, closable):
        self.to_close.append(closable)

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
        w = Widget()
        b = Button()
        w.walk()
        self.settings = Settings(self.music)
        self.add_widget(self.help)
        self.add_widget(self.settings)

    def on_win(self):
        for c in self.to_close:
            c()
        self.to_close = []
        self.add_widget(Win(self, [self.board, self.help, self.settings]))




class PuzzleApp(App):

    def build(self):
        # Window.size = (300, 550)
        return PuzzleGame()


if __name__ == '__main__':
    PuzzleApp().run()
