input = open("in").readlines();

combo = 50
p1 = 0
p2 = 0
for i in input:
    c = combo
    v = int(i.replace(*'L-').replace(*'R+'))
    combo += v
    p2 += int(abs(combo/100)) + (combo == 0) + (combo < 0 and c != 0)
    combo %= 100
    p1+=combo==0

print(p1, p2, combo)
