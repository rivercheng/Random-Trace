import math

def mean(xs):
    total = 0
    count = 0
    for x in xs:
        total += x
        count += 1
    return total * 1.0 / count

def sample_standard_deviation(xs, mean):
    total = 0
    count = 0
    for x in xs:
        total += (x-mean)*(x-mean)
        count += 1
    return math.sqrt(total * 1.0 / (count - 1))

def correlation(xs, ys):
    assert(len(xs) == len(ys))
    mean_x = mean(xs)
    mean_y = mean(ys)
    s_x    = sample_standard_deviation(xs, mean_x)
    s_y    = sample_standard_deviation(ys, mean_y)

    total = 0
    for x,y in zip(xs, ys):
        total += (x-mean_x) * (y-mean_y)

    return total * 1.0 / ((len(xs) - 1) * s_x * s_y)

if __name__ == "__main__":
    xs = [1, 2, 3]
    ys = [1, 2, 3]
    print correlation(xs, ys)

    xs = [1, 2, 3]
    ys = [1.1, 1.9, 2.9]
    print correlation(xs, ys)

    xs = [1, 2, 3]
    ys = [1.1, 2.2, 3.3]
    print correlation(xs, ys)

    xs = [1, 2, 3]
    ys = [2, 4, 6]
    print correlation(xs, ys)


