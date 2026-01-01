import re
from functools import reduce
from operator import iconcat

l=[i.split('-') for i in re.findall('[0-9]+-[0-9]+', open('in').read())]

def leftpad(a, n, c):
    return (n - len(a)) * c + a

def fill_in(a, b):
    if a == '' or b == '': return ''
    r = ''
    for i,c in enumerate(a):
        if (c != '.' and c != b[i] and b[i] != '.'):
            return ''
        r += c if c != '.' else b[i]
    return r

def chunks(s, n):
    n = len(s)//n
    return [s[i:i+n] for i in range(0, len(s), n)]

def get_invalid_ids(a, b, n = 2):
    # Checking
    if len(a) == len(b) and len(b) % n != 0:
        return [0]

    # Pruning
    if len(a) % n != 0:
        a = str('1' + '0' * len(a))
    if len(b) % n != 0:
        b = str('9' * (len(b) - 1))

    # Make the pattern
    if (len(a) == len(b)):
        i = 0
        while a[i] == b[i]: i += 1
        pat = a[:i] + '.' * (len(b) - i)
    else:
        pat = '.' * len(b)

    if len(pat) % n != 0:
        pat = pat[1:]

    # Check the pattern
    patchunk = chunks(pat, n)
    if reduce(fill_in, patchunk) == '': return [0]

    # Apply the pattern
    rpat = patchunk[0]

    rp = rpat.count('.')
    if rp == 0: return [int(rpat * n)] if int(a) <= int(rpat * n) <= int(b) else []

    # Smarter brute force
    ai, bi = int(a), int(b)
    ids = []
    for i in range(10**(rp-1), 10**rp):
        id = int(rpat.replace('.'*rp, str(i)) * n)
        if ai <= id <= bi:
            ids.append(id)
        elif id > bi:
            break

    return ids

p1,p2 = 0,0
for i in l:
    print((*i,), p1, p2)
    p1 += sum(get_invalid_ids(*i))
    p2 += sum(set(reduce(iconcat,[get_invalid_ids(*i, n) for n in range(2, len(i[1])+1)],[])))
print(p1, p2)
