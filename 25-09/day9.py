import shapely

input = [(int(i.split(',')[0]), int(i.split(',')[1])) for i in open('in').readlines()]
poly = shapely.Polygon(input)

def dist(a, b):
    return (abs(a[0]-b[0])+1) * (abs(a[1]-b[1])+1)

p1, p2 = 0, 0
for i, a in enumerate(input):
    for b in input[i + 1:]:
        d = dist(a, b)
        if d > p1:
            p1 = d
        if d > p2 and poly.contains(shapely.Polygon([a, (a[0], b[1]), b, (b[0], a[1])])):
            print(d)
            p2 = d

print(p1, p2)