import random


def left(r, index):
    i, j = index
    while j >= 0 and r[i][j] < 0:
        yield i, j
        j -= 1

def right(r, index):
    i, j = index
    while j <= 6 and r[i][j] < 0:
        yield i, j
        j += 1

def up(r, index):
    i, j = index
    while i >= 0 and r[i][j] < 0:
        yield i, j
        i -= 1

def down(r, index):
    i, j = index
    while i <= 6 and r[i][j] < 0:
        yield i, j
        i += 1

def collision_left(r, index):
    i, j = index
    while j >= 0  and r[i][j] < 0:
        if r[i][j] == -2:
            return True
        j -= 1
    return False


def collision_right(r, index, lamp_aware=False):
    i, j = index
    while j <= 6  and r[i][j] < 0:
        if r[i][j] == -2:
            return True
        j += 1
    return False

def collision_up(r, index, lamp_aware=False):
    i, j = index
    while i >= 0  and r[i][j] < 0:
        if r[i][j] == -2:
            return True
        i -= 1
    return False

def collision_down(r, index, lamp_aware=False):
    i, j = index
    while i <= 6 and r[i][j] < 0:
        if r[i][j] == -2:
            return True
        i += 1
    return False

def count_lit_cells(r, index):
    return len(list(left(r, index))) + \
           len(list(right(r, index))) + \
           len(list(up(r, index))) + \
           len(list(down(r, index)))

def empty_cells(r):
    for i, row in enumerate(r):
        for j, c in enumerate(row):
            if c == -1:
                yield i, j

def lamps_candidates(r):
    l = [(ij, count_lit_cells(r, ij)) for ij in empty_cells(r)]
    l.sort(key=lambda x: x[1],reverse=True)
    return [x[0] for x in l]

def gen_matrix_wis_black_cells():
    r = []
    black_cells = []
    for i in range(7):
        r += [[]]
        for j in range(7):
            r[i] += random.sample([-1, 0], 1)
            if r[i][j] == 1:
                black_cells += [(i, j)]
    return r


def is_lamp_collision(r, ij):
    if collision_left(r, ij):
        return True
    elif collision_right(r, ij):
        return True
    elif collision_up(r, ij):
        return True
    elif collision_down(r, ij):
        return True
    else:
        return False

def place_lamps(r):
    candidates = lamps_candidates(r)
    for c in candidates:
        if not is_lamp_collision(r, c):
            r[c[0]][c[1]] = -2
    return r

def fill_constrains(r):
    for i, lc in enumerate(r):
        for j, c in enumerate(lc):
            count = 0
            if c == 0:
                for e in [(0,1), (1,0), (0,-1), (-1,0)]:
                    if r[min(max(i - e[0], 0), 6)][min(max(j - e[1], 0), 6)] == -2:
                        count+=1
                    r[i][j] = count
    return r


def lamps_room():
    r = gen_matrix_wis_black_cells()
    r = place_lamps(r)
    r = fill_constrains(r)
    pprint_room(r)
    return r


def pprint_room(room, fmt=None):
    for row in room:
        for cell in row:
            if fmt is not None:
                print(fmt(cell), end=' ')
            else:
                print(cell, end=' ')
        print()

def test_collisions():
    r = [[-1, -1, -2, -1, -2, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -1, -2, -1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -1, -2, -1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1]]

    assert collision_left(r, (0, 3))
    assert collision_right(r, (0, 3))
    assert not collision_left(r, (1, 1))
    assert not collision_right(r, (1, 1))
    #
    assert collision_up(r, (3, 3))
    assert collision_down(r, (3, 3))
    assert not collision_up(r, (1, 1))
    assert not collision_down(r, (1, 1))
    #
    assert not collision_up(r, (0, 0))
    assert not collision_left(r, (0, 0))
    assert not collision_down(r, (6, 6))
    assert not collision_right(r, (6, 6))


def test_count():
    r = [[-1, -1, -2, -1, -2, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -1, -2, -1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -1, -2, -1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1],
         [-1, -1, -1, -1, -1, -1, -1]]

    assert len(list(left(r, (0, 3)))) == 1
    assert len(list(right(r, (0, 3)))) == 1
    assert len(list(left(r, (1, 1)))) == 6
    assert len(list(right(r, (1, 1)))) == 2
    #
    # assert up(r, (3, 3))
    # assert down(r, (3, 3))
    # assert up(r, (1, 1))
    # assert down(r, (1, 1))
    # #
    # assert up(r, (0, 0))
    # assert left(r, (0, 0))
    # assert down(r, (6, 6))
    # assert right(r, (6, 6))


if __name__ == '__main__':
    room = lamps_room()
    for i in room:
        print(i)

