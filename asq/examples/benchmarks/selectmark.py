
import sys
from timeit import Timer

from asq.initiators import query
from asq.selectors import a_

class Foo(object):
    def __init__(self):
        self.value = 42

items = []

def setup():
    for i in range(1000000):
        items.append(Foo())

def bench():
    results = query(items).select(a_("value")).to_list()

def main():
    setup()
    t = Timer("bench()", "from __main__ import bench")
    print(min(t.repeat(5, 1)))
    return 0

if __name__ == '__main__':
    sys.exit(main())