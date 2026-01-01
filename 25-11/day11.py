from functools import cache

paths = {l[:3]: l[5:].split() for l in open('in').readlines()}

@cache
def get_paths(start):
    if start == 'out':
        return 1

    return sum(get_paths(i) for i in paths[start])

@cache
def get_paths2(start, fft = False, dac = False):
    fft |= start == 'fft'
    dac |= start == 'dac'

    if start == 'out':
        return fft and dac

    ret = 0
    for i in paths[start]:
        ret += get_paths2(i, fft, dac)

    return ret

print(get_paths('you'), get_paths2('svr'))
