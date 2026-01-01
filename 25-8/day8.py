from math import prod

N_CONN = 1000
input = [tuple(map(int, l.split(','))) for l in open('in').readlines()]
total = len(input)

dists = []
for i, (x, y, z) in enumerate(input[:-1]):
    for next in input[i + 1:]:
        d = (x - next[0])**2 + (y - next[1])**2 + (z - next[2])**2
        dists.append((d, (x, y, z), next))

dists.sort(key = lambda a: a[0])

p1 = 0
cid = 1
circuit_map, circuits = {}, {}
for n, dist in enumerate(dists):
    _, a, b = dist

    ac, bc = circuits.get(a), circuits.get(b)
    ncid = ac or bc or cid
    if ac != bc and None not in [ac, bc]:
        ncid = ac
        for next in circuit_map[bc]:
            circuits[next] = ac
            circuit_map[ac].add(next)
        circuit_map[bc] = set()
    else:
        if ncid == cid:
            cid += 1
            circuit_map[ncid] = set()

        circuits[a] = ncid
        circuit_map[ncid].add(a)
        circuits[b] = ncid
        circuit_map[ncid].add(b)

    if total <= 0:
        print(total)

    n += 1
    if n == N_CONN:
        p1 = prod(sorted(len(i) for i in circuit_map.values())[-3:])

    if total == len(circuit_map[ncid]):
        print(p1, a[0] * b[0])
        break
