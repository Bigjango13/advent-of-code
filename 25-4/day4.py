input = [[*l.strip()] for l in open('in').readlines()]
tryget = lambda a,b: input[a][b] if 0 <= a < len(input) and 0 <= b < len(input[a]) else '.'

p1,p2 = 0,0
rolls = []
while p1 == 0 or len(rolls) > 0:
    # Remove the last round
    while len(rolls) > 0:
        y,x = rolls.pop()
        input[y][x] = '.'

    for y in range(len(input)):
        if input[y].count('@') == 0:
            continue
        for x in range(len(input[y])):
            if input[y][x] != '@': continue
            if [tryget(y+yy,x+xx) for yy,xx in ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1))].count('@') < 4:
                rolls.append((y, x))

    p2 += len(rolls)

    # Part 1 is just part 2 but stop before removing anything
    if p1 == 0:
        p1 = p2

print(p1, p2)
