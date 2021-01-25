import random
from typing import Optional

from Lamp_room import lamps_room
from camp import room_camp, pprint_room

from cell import EmptyCell, SwitchCell, ManCell, TentCell, PrintCell, TreeCell, LampCell


class Room:
    def __init__(self):
        self.h = 7
        self.w = 7
        self.r = self._generate()

    def _generate(self):
        raise NotImplementedError

    def generate_knights_liars(self):
        r = []
        for i in range(7):
            r += [[]]
            for j in range(7):
                r[i] += [EmptyCell()]
        for j in range(7):
            r[3][j] = ManCell(self, j)

        for j in range(7):
            r[2][j] = PrintCell((2, j), r[3][j].say(r[3][(j+1)%7]))


        for c in r[3]:
            print(c.I, end=', ')
        print()
        for i, c in enumerate(r[3]):
            print(c.say(r[3][(i+1) % 7]), end=', ')
        print()
        return r

    def activate_cell(self, i, j):
        self.r[i][j].activate()

    def activate_cell_neighbours(self, i, j):
        self.get_cell(i, j).invert_neighbours(i, j)

    def get_cell(self, i, j) -> Optional[SwitchCell]:
        if i<=6:
            if j<=6:
                return self.r[i][j]
        else:
            return None

    def get_neighbours(self, i, j):
        l = [(-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (0, 0)]
        for di, dj in l:
            ii = (i + di)%7
            jj = (j + dj)%7
            yield self.get_cell(ii, jj)

    def checks(self):
        raise NotImplementedError

    def say(self):
        raise NotImplementedError


class LampRoom(Room):

    def say(self):
        return """
    Фонари ("Light Up", "Akari", "Bijutsukan") – это логическая головоломка.
    Игровое поле состоит из белых и черных клеток; в некоторых черных 
    клетках расположены числа. Необходимо разместить "светильники" в 
    белых клетках таким образом, чтобы все игровое поле было освещено, 
    но фонари не "светили" бы друг на друга. Свет фонаря распространяется 
    по горизонтали и по вертикали, но может быть заблокирован черной 
    клеткой. В черной клетке может находиться число от 0 до 4, указывая, 
    сколько фонарей должно быть размещено рядом с ней (не учитываются 
    фонари, помещенные по диагонали от этой черной клетки).
        """

    def checks(self):
        pprint_room(self.r)
        tf = []
        for i in self.r:
            for j in i:
                tf += [j.check()]
        return all(tf)

    def _generate(self):
        rcn = lamps_room()
        r = []
        for i in range(7):
            r += [[]]
            for j in range(7):
                r[i] += [None]
        for i, s_cell in enumerate(rcn):
            for j, cell in enumerate(s_cell):
                if cell == -2:
                        r[i][j] = LampCell(True)
                elif cell == -1:
                        r[i][j] = LampCell(False)
                if cell >= 0:
                    r[i][j] = PrintCell((i, j), cell)
        return r


class CampRoom(Room):

    def say(self):
        return"""
        
 Лагерь ("Tents", "Tents and Trees") 
 представляет собой квадратную или прямоугольную сетку,
 некоторые клетки которой содержат "деревья". 
 Необходимо разместить рядом с деревьями "палатки", 
 соблюдая следующие правила:
 Число палаток равняется числу деревьев.
 Каждая палатка располагается рядом со "своим" деревом
 по горизонтали или вертикали, но не по диагонали. 
 Если это условие выполнено, расположение по отношению
 к "чужим" деревьям значения не имеет.
 Числа сбоку и сверху означают,
 сколько палаток находится в этой строке или столбце.
        """

    def checks(self):
        pprint_room(self.r)
        tf = []
        for i in self.r:
            for j in i:
                tf += [j.check()]
        return all(tf)

    def _generate(self):
        rcn = room_camp()
        r = []
        for i in range(7):
            r += [[]]
            for j in range(7):
                r[i] += [None]
        for i, s_cell in enumerate(rcn):
            for j, cell in enumerate(s_cell):
                if i != 0 and j != 0 and cell != 3:
                    if cell == 2:
                        r[i][j] = TentCell(True)
                    else:
                        r[i][j] = TentCell(False)
                if  i == 0 or j == 0:
                    r[i][j] = PrintCell((i, j), cell)
                if i != 0 and j != 0 and cell == 3:
                    r[i][j] = TreeCell()


        return r



class KnightsRoom(Room):

    def say(self):
        return """На острове Буяне жили 7 человек, каждый 
из которых был либо рыцарем либо лжецом,
они встали в круг. Рыцари оворят только 
правду, лжецы всегда только лгут. 
Каждому человеку в кругу задали вопрос:
«кто твой сосед справа: рыцарь или лжец?»
При этом ответы всех людей о правом 
соседе были записаны в следующем 
формате: 1 – рыцарь 0 – лжец. 
Последний спрошенный человек отвечал 
на вопрос о первом.
        """
    def checks(self):
        tf = []
        for i in self.r[3]:
            tf += [i.check()]
        return all(tf)

    def _generate(self):
        return self.generate_knights_liars()


class SwitchRoom(Room):
    def say(self):
        return 'Сделай, всё синим!'

    def _generate(self):
        return self._generate3x3()

    def checks(self):
        tf = []
        for  row in self.r:
            for cell in row:
                tf += [cell.check()]
        return all(tf)

    def _generate3x3(self):
        r = []
        for i in range(7):
            r += [[]]
            for j in range(7):
                r[i] += [EmptyCell()]
        for i in range(3 - 1, 3 + 2):
            for j in range(3 - 1, 3 + 2):
                if bool(random.randint(0,1)):
                    r[i][j] = SwitchCell(self)
                    r[i][j].activate()
                else:
                    r[i][j] = SwitchCell(self)
        return r

    def _generate7x7(self):
        r = []
        for i in range(7):
            r += [[]]
            for j in range(7):
                r[i] += [SwitchCell(self)]
        return r
    def _generate5x5(self):
        r = []
        for i in range(7):
            r += [[]]
            for j in range(7):
                r[i] += [EmptyCell()]
        for i in range(3 - 2, 3 + 3):
            for j in range(3 - 2, 3 + 3):
                if bool(random.randint(0,1)):
                    r[i][j] = SwitchCell(self)
                    r[i][j].activate()
                else:
                    r[i][j] = SwitchCell(self)
        return r

if __name__ == '__main__':
    room = Room()
