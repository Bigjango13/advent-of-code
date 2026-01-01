input = open('in').readlines()

b = input.index('\n')
fresh = [(int(i.split('-')[0]),int(i.split('-')[1])) for i in input[:b]]
ids = [int(i)for i in input[b+1:]]

changed = True
while changed:
    changed = False

    for i, ab in enumerate(fresh):
        a, b = ab

        for ii, aabb in enumerate(fresh):
            if i == ii: continue

            aa, bb = aabb
            if (a <= aa and aa <= b) or (a <= bb and bb <= b):
                a = min(a, aa)
                b = max(b, bb)
                fresh[i] = fresh[ii] = a,b
                changed = True
    fresh = list(set(fresh))

p1 = 0
for id in ids:
    p1 += any(a <= id <= b for (a, b) in fresh)

p2 = sum((b-a)+1 for (a,b) in fresh)

print(p1, p2)
