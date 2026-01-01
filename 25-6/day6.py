from math import prod

input = [i for i in open('in').readlines()]

# Part 1
p1input = list(zip(*[i.strip().split() for i in input]))
p1 = 0
for i in p1input:
    if i[-1] == '*':
        p1 += prod(int(j) for j in i[:-1])
    elif i[-1] == '+':
        p1 += sum(int(j) for j in i[:-1])

# Part 2
p2 = 0
op = ' '
c=0
for x in range(len(input[0]) - 1):
    n = ''.join([input[y][x] for y in range(len(input))])

    if n.count(' ') == len(n):
        # Empty row
        op = ' '
        p2 += c
        c=0
    elif n[-1] in '+*':
        # Operator specified
        op = n[-1]
        if op == '*': c = 1
        n = n[:-1]

    # Use the number
    if op == '+':
        c += int(n)
    elif op == '*':
        c *= int(n)

p2 += c

print(p1, p2)