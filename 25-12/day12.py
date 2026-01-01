input = open('in').readlines()

# Parse input
def to_shape(a, b, c):
    return [
        (x, y)
        for y,v in enumerate([a, b, c])
        for x,vv in enumerate(v) if vv == '#'
    ]

def parse_input():
    lindex = len(input) - 1 - input[::-1].index('\n')
    gifts = [to_shape(*i[3:].split()) for i in ''.join(input[:lindex]).split('\n\n')]
    boxes = [(
            *map(int, i.split(': ')[0].split('x')),
            [*map(int, i.split(': ')[1].split())]
    ) for i in input[lindex + 1:]]

    return gifts, boxes

gifts, boxes = parse_input()

p1 = 0
for bx, by, ngifts in boxes:
    p1 += sum(v*len(gifts[i]) for i,v in enumerate(ngifts)) <= bx * by

print(p1)
