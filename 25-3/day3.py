input=open('in').readlines()

p1,p2 = 0,0
ln = 12
for l in input:
    l = l.strip()

    # P1
    a = sorted(l[:-1])[-1]
    b = sorted(l[l.index(a)+1:])[-1]
    p1 += int(a+b)

    # P2
    indexiis = []
    cap = len(l) - (ln-1)
    for i in range(ln):
        off = (indexiis[-1]+1) if i > 0 else 0
        max = sorted(l[off:cap+i])[-1]
        indexiis.append(l.index(max, off))

    p2 += int(''.join([l[indexiis[i]] for i in range(ln)]))

print(p1, p2)
