import random


class EmptyCell:
    def __init__(self):
        pass

    def activate(self):
        pass

    def check(self):
        return True


class TreeCell(EmptyCell):
    def __init__(self):
        super().__init__()

    def activate(self):
        pass

    def check(self):
        return True

    def __str__(self):
        return '|'  # '\U0001F332'


class PrintCell(EmptyCell):
    def __init__(self, ij, ws):
        super().__init__()
        self._active = True
        self.ij = ij
        self.ws = ws

    def cords(self):
        return self.ij

    def is_active(self):
        return self._active

    def check(self):
        return True

    def activate(self):
        pass

    def say(self):
        return self.ws

    def __str__(self):
        return f'{self.say()}'


class TentCell(EmptyCell):
    def __init__(self, tr_s):
        super().__init__()
        self._active = False
        self.tr_s = tr_s

    def is_active(self):
        return self._active

    def check(self):
        return self._active == self.tr_s

    def activate(self):
        self._active = not self._active

    def __str__(self):
        if self.is_active():
            return 'A'
        else:
            return ' '


class LampCell(EmptyCell):
    def __init__(self, tr_s):
        super().__init__()
        self._active = False
        self.tr_s = tr_s

    def is_active(self):
        return self._active

    def check(self):
        return self._active == self.tr_s

    def activate(self):
        self._active = not self._active

    def __str__(self):
        if self.is_active():
            return 'A'
        else:
            return ' '


class SwitchCell(EmptyCell):
    def __init__(self, room):
        super().__init__()
        self._room = room
        self._active = False

    def check(self):
        return self._active

    def activate(self):
        self._active = not self._active

    def is_active(self):
        return self._active

    def invert_neighbours(self, i, j):
        for cell in self._room.get_neighbours(i, j):
            cell.activate()


class ManCell(EmptyCell):
    def __init__(self, room, n):
        super().__init__()
        self._active = False
        self.I = random.randint(0, 1)
        self.n = n

    def activate(self):
        self._active = not self._active

    def is_active(self):
        return self._active

    def i_am(self):
        return self.I

    def say(self, naig):
        d = {}
        d[0, 1] = 0
        d[1, 0] = 0
        d[1, 1] = 1
        d[0, 0] = 1
        return f'{d[self.I, naig.I]}'

    def check(self):
        if bool(self.I) == self._active:
            return True
        else:
            return False
