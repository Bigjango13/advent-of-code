from fractions import Fraction
from math import gcd, prod
from itertools import combinations, product
from functools import reduce
from operator import xor

def parse_line(l):
    p = l.strip().split()
    lights = int(p[0][1:-1][::-1].replace('.', '0').replace('#', '1'), 2)
    joltage = [int(i) for i in p[-1][1:-1].split(',')]
    buttons = [sum(1<<int(j) for j in i[1:-1].split(',')) for i in p[1:-1]]
    return lights, buttons, joltage

input = [parse_line(i) for i in open('in').readlines()]

def getcombo(lights, buttons):
    for l in range(2, len(buttons) + 1):
        for b in combinations(buttons, l):
            if reduce(xor, b) == lights:
                return l

def addjolts(button, jolts, m = 1):
    return [jolts[i] + ((button >> i) & 1)*m for i in range(len(jolts))]

Fraction.__repr__ = lambda s: format(s, '')
def print_matrix(matrix):
    for row in matrix:
        n = next((i for i,v in enumerate(row) if v != 0))
        print(end=f'P_{{{n+1}}}=\\frac{{{row[-1]}-\\left(')
        for i, v in enumerate(row[:-1]):
            if i <= n: continue
            if v != 0:
                print(
                    end=f'{"+"if v>0 else""}{v if abs(v)!=1 else{1:"",-1:"-"}[v]}P_{{{i+1}}}'
                )
        print(f'\\right)}}{{{row[n]}}}')
    for row in matrix:
        print(end='\\left(')
        for i,v in enumerate(row[:-1]):
            if v != 0:
                print(
                    f'{"+"if v>0 else""}{v if abs(v)!=1 else{1:"",-1:"-"}[v]}p_{{{i+1}}}',
                    end=''
                )
        print(f',{row[-1]}\\right)')

def to_matrix(buttons, jolts):
    matrix = []
    for i,jolt in enumerate(jolts):
        sys = []
        for button in buttons:
            sys.append((button >> i) & 1)
        matrix.append(sys + [jolt])
    return matrix

def getranges(maxes, matrix):
    drange = (0, float('inf'))
    for row in matrix:
        # Negatives screw stuff up
        if row[:-1] != 0 and not all(r >= 0 for r in row): continue
        sum_ = 0
        val = (-1, -1)
        for i,r in enumerate(row[:-1]):
            if r == 0: continue
            if val == (-1, -1): val = (i, r)
            sum_ += r
            cr = maxes.get(i, drange)
            if int(row[-1] / r) < cr[1]:
                maxes[i] = (cr[0], int(row[-1] / r))
        # Min
        if sum_ == val[1]:
            cr = maxes.get(val[0], drange)
            if int(row[-1]/sum_) > cr[0]:
                assert int(row[-1]/sum_) == row[-1]/sum_
                maxes[val[0]] = (int(row[-1] / sum_), cr[1])

    return maxes

def div(a, b):
    ret = Fraction(a, b)
    if ret.is_integer(): return int(ret)
    return ret

def mrow(a, m): return [m*aa for aa in a]
def madd(a, b): return [aa+bb for aa,bb in zip(a,b)]
def gaussian_elimination(matrix):
    if len(matrix) == 0: return []
    if not any(matrix[0]): return gaussian_elimination(matrix[1:])
    c = next((i for i in range(len(matrix[0])) if any(matrix[j][i] for j in range(len(matrix)))))

    if matrix[0][c] == 0:
        for i in range(1, len(matrix)):
            if matrix[i][c] != 0:
                matrix[0], matrix[i] = matrix[i], matrix[0]
                break
    elif matrix[0][c] != 1:
        for i in range(1, len(matrix)):
            if matrix[i][c] == 1:
                matrix[0], matrix[i] = matrix[i], matrix[0]
                break

    # Make sure the leading line is a 1
    if matrix[0][c] != 1:
        a = matrix[0][c]
        matrix[0] = mrow(matrix[0], div(1, a))

    if len(matrix) == 1:
        return matrix

    for i in range(1, len(matrix)):
        if matrix[i][c] != 0:
            matrix[i] = madd(matrix[i], mrow(matrix[0], -div(matrix[i][c],matrix[0][c])))

    return [matrix[0], *gaussian_elimination(matrix[1:])]

# Reduces the possibilities of the matrix, can occasionally solve it entirely
def possiblities(row):
    if any(r < 0 for r in row): return float('inf')
    return prod(r*row[-1] for r in row[:-1] if r != 0) - row[-1]

def reduce_possible(matrix):
    changed = False
    for ri,row in enumerate(matrix):
        for row2 in matrix[ri + 1:]:
            pos = possiblities(row)
            pos1 = possiblities(madd(row, row2))
            pos2 = possiblities(madd(row, mrow(row2, -1)))
            if pos1 < pos and pos1 <= pos2:
                matrix[ri] = madd(row, row2)
                changed = True
            elif pos2 < pos:
                matrix[ri] = madd(row, mrow(row2, -1))
                changed = True

    if changed: return reduce_possible(matrix)
    return matrix

# Solves a single row using known vals
def solve_row(row, preval, n):
    return div(
        (row[-1] - sum(m*preval[i] for i, m in enumerate(row[:-1]) if m != 0 and i != n)),
        row[n]
    )

# Returns the indexes of the free vars
def get_free(matrix):
    ret = []
    nvars = len(matrix[0]) - 1
    rowi = 0
    for i in range(nvars):
        if rowi < len(matrix) and matrix[rowi][i] != 0:
            rowi += 1
        else:
            ret.append(i)
    return ret

# Back substitution on the matrix, using `preval` for free variables
def backsub_simple(matrix, preval):
    nvals = preval
    for row in matrix[::-1]:
        n = next((i for i,v in enumerate(row) if v != 0))

        nval = solve_row(row, preval, n)
        # Invalid combo, from bad guess
        if nval != int(nval) or nval < 0:
            return []

        nvals[n] = nval

    return [*nvals.values()]

# Brute force the min values of the free variables for back substitution
def backsub(matrix, maxes):
    if len(matrix[0]) - 1 <= len(matrix):
        return backsub_simple(matrix, {})

    # Get the values that need to be guessed
    guessedn = get_free(matrix)
    guessedc = [range(maxes[i][0], maxes[i][1] + 1) for i in guessedn]

    print(
        "Checking", prod(len(i) for i in guessedc), "combos:",
        [*zip(guessedn, guessedc)]
    )
    bestcombo = (float('inf'), [])
    for pre in product(*guessedc):
        ret = backsub_simple(matrix, {a:b for a,b in zip(guessedn, pre)})
        if ret and sum(ret) < bestcombo[0]:
            bestcombo = (sum(ret), ret)

    assert bestcombo[0] not in [float('inf'), 0]
    return bestcombo[1]

p2 = 0
for i in range(len(input)):
    m = to_matrix(input[i][1], input[i][2])
    #print(*m, sep='\n')
    maxes = getranges({}, m)
    m = gaussian_elimination(m)
    maxes = getranges(maxes, m)
    pmaxes = {a:b for a,b in maxes.items()}
    #print('Reduced:',*m, sep='\n')
    m = reduce_possible(m)
    maxes = getranges(maxes, m)
    #print("^--------v")
    #print(*m, sep='\n')
    #print(pmaxes, maxes, sep='\n')
    #print_matrix(m)
    v = backsub(m, maxes)
    p2 += sum(v)
    #print(sum(v), v, p2, '\n')

# Part 1
p1 = 0
for lights, buttons, joltage in input:
    if lights in buttons:
        p1 += 1
    else:
        p1 += getcombo(lights, buttons)

print(p1, p2)
