input = open('in').readlines()

touched = {}
def gettl(y, x):
    a = touched[(y, x)]
    if type(a) == int:
        return a
    return gettl(*a)

p1 = 0
def decent(y, x):
    global p1
    oy, ox = y, x
    while y < len(input):
        if touched.get((y, x)) is not None:
            # Merge timelines
            touched[(oy, ox)] = gettl(y, x)
            return touched[(oy, ox)]

        if input[y][x] == '^':
            p1 += 1
            touched[(oy, ox)] = decent(y, x + 1) + decent(y, x - 1)
            return touched[(oy, ox)]

        touched[(y, x)] = (oy, ox)
        y += 1

    touched[(oy, ox)] = 1
    return 1

fy, fx = 0, input[0].index('S')
p2 = decent(fy, fx)
print(p1, p2)
