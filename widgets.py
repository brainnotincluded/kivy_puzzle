import random

from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from cell import ManCell, TentCell, EmptyCell, TreeCell, PrintCell, LampCell, SwitchCell
from room import SwitchRoom, KnightsRoom, CampRoom, LampRoom


class Win(AnchorLayout):
    def __init__(self, game, to_remoove, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        for i in range(len(to_remoove)):
            self.game.remove_widget(to_remoove[i])
        self.add_widget(Button(text='Congratulation! More?', on_press=self.on_press))

    def on_press(self, x):
        self.game.remove_widget(self)
        self.game._init_game()




class Cell(Button):
    def __init__(self, game, ij, room, image_active, image_inactive, **kwargs):
        super().__init__(**kwargs)
        self.border = (0, 0, 0, 0)
        self.image_active = image_active
        self.image_inactive = image_inactive
        self.background_normal = image_inactive
        self.size_hint = 1, None
        self.ij = ij
        self.room = room
        self.game = game

    def on_size(self, w, h):  # hook size set and make height equal to width
        if w == h:
            return
        self.height = self.width

    def on_press(self):
        self.room.r[self.ij[0]][self.ij[1]].activate()
        if self.room.r[self.ij[0]][self.ij[1]].is_active():
            self.background_normal = self.image_active
            self.background_down = self.image_active
        else:
            self.background_normal = self.image_inactive
            self.background_down = self.image_inactive
            self.room.checks()
        if self.room.checks():
            self.game.on_win()


class KnightLiarCellV(Cell):
    def __init__(self, game, ij, room, **kwargs):
        super().__init__(game, ij, room, 'images/knight.png', 'images/liar.png', **kwargs)


class TentCellV(Cell):
    def __init__(self, game, ij, room, **kwargs):
        super().__init__(game, ij, room, 'images/tent.png', 'images/grass.png', **kwargs)


class LampCellV(Cell):
    def __init__(self, game, ij, room, **kwargs):
        super().__init__(game, ij, room, 'images/lamp1.png', 'images/lamp.png', **kwargs)


class SwitchCellV(Cell):
    def __init__(self, game, ij, room, **kwargs):
        super().__init__(game, ij, room, 'images/tile1.png', 'images/tile2.png', **kwargs)


class PrintCellV(Cell):
    def __init__(self, game, ij, room, **kwargs):
        super().__init__(game, ij, room, 'images/black.png', 'images/black.png', **kwargs)
        self.color = (0.9, 0.9, 0.9, 1)
        self.text = f'{self.room.r[self.ij[0]][self.ij[1]].say()}'


class EmptyCellV(Cell):
    def __init__(self, game, ij, room, **kwargs):
        super().__init__(game, ij, room, 'images/tile.png', 'images/tile.png', **kwargs)


class TreeCellV(Cell):
    def __init__(self, game, ij, room, **kwargs):
        super().__init__(game, ij, room, 'images/tree1.png', 'images/tree1.png', **kwargs)


class Board(GridLayout):
    def __init__(self, game, **kwargs):
        self.room = random.sample([LampRoom, SwitchRoom, KnightsRoom, CampRoom], 1)[0]()
        self.r = self.room.r
        super().__init__(**kwargs)
        self.cols = 7
        self.rows = 7
        for i in range(self.cols):
            for j in range(self.rows):
                if isinstance(self.r[i][j], TreeCell):
                    self.add_widget(TreeCellV(game, (i, j), self.room, **kwargs))
                elif isinstance(self.r[i][j], PrintCell):
                    self.add_widget(PrintCellV(game, (i, j), self.room, **kwargs))
                elif isinstance(self.r[i][j], TentCell):
                    self.add_widget(TentCellV(game, (i, j), self.room, **kwargs))
                elif isinstance(self.r[i][j], LampCell):
                    self.add_widget(LampCellV(game, (i, j), self.room, **kwargs))
                elif isinstance(self.r[i][j], SwitchCell):
                    self.add_widget(SwitchCellV(game, (i, j), self.room, **kwargs))
                elif isinstance(self.r[i][j], ManCell):
                    self.add_widget(KnightLiarCellV(game, (i, j), self.room, **kwargs))
                elif isinstance(self.r[i][j], EmptyCell):
                    self.add_widget(EmptyCellV(game, (i, j), self.room, **kwargs))

        with self.canvas.before:
            Color(0 / 255, 0 / 255, 75 / 255, 1)
            Rectangle(pos=(0, 0), size=(1000, 2000))
