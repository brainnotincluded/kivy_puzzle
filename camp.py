import random


def fill_constraints(r_7x7):
    for i in range(1, 7):
        r_7x7[i][0] = r_7x7[i].count(2)

    for j in range(1, 7):
        s = 0
        for i in range(1, 7):
            if r_7x7[i][j] == 2:
                s += 1
        r_7x7[0][j] = s
    return r_7x7

def validate(tents_indices):
    for ti0 in tents_indices:
        for ti1 in tents_indices:
            if ti0 > ti1:
                di = abs(ti0[0]-ti1[0])
                dj = abs(ti0[1] - ti1[1])
                if di <= 1 and dj <= 1:
                    raise ValueError(f'найдены соседние палатки:{ti0}, {ti1}')


def room_camp_7x7(r_6x6):
    r = []
    for i in range(7):
        r += [[]]
        for j in range(7):
            r[i] += [0]
            if i > 0 and j > 0:
                r[i][j] = r_6x6[i-1][j-1]
    return r


def place(i, j, tents_indices):
    ltft = []
    sample = random.sample([1, 1, 2], 1)[0]
    if sample == 2:
        for ti in tents_indices:
            ltft += [not ((i, j) == (ti[0] - 1, ti[1] - 1) or (i, j) == (ti[0] - 1, ti[1]) or (i, j) == (
            ti[0], ti[1] - 1) or (i, j) == (ti[0] + 1, ti[1] - 1) or (i, j) == (ti[0] - 1, ti[1] + 1) or (i, j) == (
                          ti[0] + 1, ti[1] + 1) or (i, j) == (ti[0] + 1, ti[1]) or (i, j) == (ti[0], ti[1] + 1))]
        if all(ltft):
            return 2
        else:
            return 1
    else:
        return 1

def room_camp():
    r = []
    tents_indices = []
    trees_indices = []
    for i in range(6):
        r += [[]]
        for j in range(6):
            ct = place(i, j, tents_indices)
            r[i] += [ct]
            if r[i][j] == 2:
                tents_indices += [(i, j)]
    for tent_index in tents_indices:
        def gen_mtis(ti):
            for pi, pj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                pi += ti[0]
                pj += ti[1]
                in_bounds = 0 <= pi <= 5 and 0 <= pj <= 5
                p = pi, pj
                collision = p in trees_indices or p in tents_indices
                if in_bounds and not collision:
                    yield pi, pj
        try:
            candidate_trees = list(gen_mtis(tent_index))
            i, j = random.choice(candidate_trees)
            trees_indices += [(i, j)]
            r[i][j] = 3
        except:
            return room_camp()
        room = fill_constraints(room_camp_7x7(r))
    validate(tents_indices)
    pprint_room(room)
    return room


def pprint_room(room, fmt=None):
    for row in room:
        for cell in row:
            if fmt is not None:
                print(fmt(cell), end=' ')
            else:
                print(cell, end=' ')
        print()


if __name__ == '__main__':
    room = room_camp()

    for i in room:
        print(i)