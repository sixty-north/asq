def times_two(x):
    return 2 * x


def times(x, y):
    return x * y


def infinite():
    i = 0
    while True:
        yield i
        i += 1


class TracingGenerator(object):

    def __init__(self):
        self._trace = []
        self._i = 0

    def __iter__(self):
        while True:
            self._trace.append(self._i)
            yield self._i
            self._i += 1

    trace = property(lambda self: self._trace)


def inc_chr(y):
    return chr(ord(y)+1)


def randgen():
    import random
    while True:
        yield random.random()
