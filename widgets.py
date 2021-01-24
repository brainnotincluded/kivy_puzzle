import random

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from cell import ManCell, TentCell, EmptyCell, TreeCell, PrintCell, LampCell, SwitchCell
from room import Room, SwitchRoom, KnightsRoom, CampRoom, LampRoom


class Cell(Button):
    def __init__(self, ij, room, image_active, image_inactive, **kwargs):
        super().__init__(**kwargs)
        # self.background_down = 'images/knight.png'
        # self.background_normal = 'images/liar.png'
        self.image_active = image_active
        self.image_inactive = image_inactive
        self.background_normal = image_inactive
        self.size_hint = None, None
        self.size = 50, 50
        self.ij = ij
        self.room = room

    def on_press(self):
        self.room.r[self.ij[0]][self.ij[1]].activate()
        if self.room.r[self.ij[0]][self.ij[1]].is_active():
            self.background_normal = self.image_active
            self.background_down = self.image_active
        else:
            self.background_normal = self.image_inactive
            self.background_down = self.image_inactive


class KnightLiarCellV(Cell):
    def __init__(self, ij, room, **kwargs):
        super().__init__(ij, room, 'images/knight.png', 'images/liar.png', **kwargs)


class TentCellV(Cell):
    def __init__(self, ij, room, **kwargs):
        super().__init__(ij, room, 'images/tent.png', 'images/grass.png', **kwargs)

class LampCellV(Cell):
    def __init__(self, ij, room, **kwargs):
        super().__init__(ij, room, 'images/lamp.png', 'images/lamp1.png', **kwargs)

class SwitchCellV(Cell):
    def __init__(self, ij, room, **kwargs):
        super().__init__(ij, room, 'images/tile1.png', 'images/tile2.png', **kwargs)


class PrintCellV(Cell):
    def __init__(self, ij, room, **kwargs):
        super().__init__(ij, room, 'images/black.png', 'images/black.png', **kwargs)
        self.color = (0.9, 0.9, 0.9, 1)
        self.text = f'{self.room.r[self.ij[0]][self.ij[1]].say()}'


class EmptyCellV(Cell):
    def __init__(self, ij, room, **kwargs):
        super().__init__(ij, room, 'images/tile.png', 'images/tile.png', **kwargs)


class TreeCellV(Cell):
    def __init__(self, ij, room, **kwargs):
        super().__init__(ij, room, 'images/tree1.png', 'images/tree1.png', **kwargs)


class Board(GridLayout):
    def __init__(self, **kwargs):
        room = random.sample([KnightsRoom], 1)[0]()
        self.r = room.r
        super().__init__(**kwargs)
        self.cols = 7
        self.rows = 7
        for i in range(self.cols):
            for j in range(self.rows):
                if isinstance(self.r[i][j], TreeCell):
                    self.add_widget(TreeCellV((i, j), room, **kwargs))
                elif isinstance(self.r[i][j],PrintCell):
                    self.add_widget(PrintCellV((i, j), room, **kwargs))
                elif isinstance(self.r[i][j],TentCell):
                    self.add_widget(TentCellV((i, j), room, **kwargs))
                elif isinstance(self.r[i][j],LampCell):
                    self.add_widget(LampCellV((i, j), room, **kwargs))
                elif isinstance(self.r[i][j], SwitchCell):
                    self.add_widget(SwitchCellV((i, j), room, **kwargs))
                elif isinstance(self.r[i][j], ManCell):
                    self.add_widget(KnightLiarCellV((i, j), room, **kwargs))
                elif isinstance(self.r[i][j], EmptyCell):
                    self.add_widget(EmptyCellV((i, j), room, **kwargs))


        with self.canvas.before:
            Color(0 / 255, 0 / 255, 50 / 255, 1)
            Rectangle(pos=(0, 0), size=(1000, 1000))
