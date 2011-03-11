import heapq
import itertools
import functools
import multiprocessing

# Temporary warning
import sys
sys.stderr.write("Warning: The asq parallel query functionality should be "
                 "considered to be alpha quality.")

from .queryable import (Queryable, identity, default)

def star(func_and_args):
    func, args = func_and_args
    return func(*args)

class ParallelQueryable(Queryable):
    '''
    A parallel version of Queryable using the multiprocessing module.
    '''
    def __init__(self, iterable, pool=None, chunksize=1):
        super(ParallelQueryable, self).__init__(iterable)

        #TODO : Support for shared pools

        self._own_pool = pool is None

        if self._own_pool:
            pool = multiprocessing.Pool()

        self._pool = pool
        self._chunksize = chunksize

    def _create(self, iterable):
        return ParallelQueryable(iterable, self._pool, self._chunksize)

    def _create_ordered(self, iterable, func=None):
        return OrderedParallelQueryable(iterable, func, self._pool, self._chunksize)

    def close(self):
        if self._own_pool:
            self._pool.close()
        super(ParallelQueryable, self).close()


    def select(self, selector):
        '''Transforms each element of a sequence into a new form.

        Each element is transformed through a selector function to produce a value for each value in the source
        sequence. The generated sequence is lazily evaluated.

        Args:
            selector: A unary function mapping a value in the source sequence to the corresponding value in the generated
                generated sequence. The argument of the selector function
                (which can have any name) is,

                Args:
                    element: The value of the element

                Returns:
                    The selected value derived from the element value

        Returns:
            A generated sequence whose elements are the result of invoking the selector function on each element of the
            source sequence.
        '''
        return self._create(self._pool.imap_unordered(selector, iter(self), self._chunksize))

    def select_with_index(self, selector):
        '''Transforms each element of a sequence into a new form, incorporating the index of the element.

        Each element is transformed through a selector function which accepts the element value and its zero-based index
        in the source sequence. The generated sequence is lazily evaluated.

        Args:
            selector: A two argument function mapping the index of a value in the source sequence and the element value
                itself to the corresponding value in the generated sequence. The two arguments of the selector function
                (which can have any names) and its return value are,

                Args:
                    index: The zero-based index of the element
                    element: The value of the element

                Returns:
                    The selected value derived from the index and element

        Returns:
            A generated sequence whose elements are the result of invoking the selector function on each element of the
            source sequence
        '''

        return self._create(self._pool.imap_unordered(star, zip(itertools.repeat(selector), enumerate(iter(self))),  self._chunksize))

    def select_many(self, projector, selector=identity):
        '''Projects each element of a sequence to an intermediate new sequence, flattens the resulting sequence into one
        sequence and optionally transforms the flattened sequence using a selector function.

        Args:
            projector: A unary function mapping each element of the source sequence into an intermediate sequence. If no
                projection function is provided, the intermediate sequence will consist of the single corresponding
                element from the source sequence. The projector function argument (which can have any name) and return
                values are,

                Args:
                    element: The value of the element

                Returns:
                    An iterable derived from the element value

            selector: An optional unary functon mapping the elements in the flattened intermediate sequence to
                corresponding elements of the result sequence. If no selector function is provided, the identity
                function is used.  The selector function argument and return values are,

                Args:
                    element: The value of the intermediate element from the concatenated sequences arising from the
                        projector function.

                Returns:
                    The selected value derived from the element value
        Returns:
            A generated sequence whose elements are the result of projecting each element of the source sequence using
            projector function and then mapping each element through an optional selector function.
        '''
        sequences = (self._create(item).select(projector) for item in iter(self))
        #print(sequences)
        # TODO: Without the list() to force evaluation multiprocessing deadlocks...
        chained_sequence = list(itertools.chain.from_iterable(sequences))
        return self._create(self._pool.imap_unordered(selector, chained_sequence, self._chunksize))

    # TODO: Replace lambda with a named module-scope function
    def select_many_with_index(self, projector=lambda i,x:[x], selector=identity):
        sequences = (self._create(item).select_with_index(projector) for item in iter(self))
        chained_sequence = itertools.chain.from_iterable(sequences)
        return self._create(self._pool.imap_unordered(selector, chained_sequence, self._chunksize))

    def select_many_with_correspondence(self, projector=lambda x:[x], selector=lambda x, y: y):
        corresponding_projector = lambda x: (x, projector(x))
        corresponding_selector = lambda x_y : selector(x_y[0], x_y[1])

        sequences = (Queryable(item).select(corresponding_projector) for item in iter(self))
        chained_sequence = itertools.chain.from_iterable(sequences)
        return self._create(self._pool.imap_unordered(corresponding_selector, chained_sequence, self._chunksize))

    def order_by(self, func=identity):
        return self._create_ordered(iter(self), func)

    # TODO: order_by_descending

    def where(self, predicate):
        partitions = realize_partitions(iter(self))
        filterer = functools.partial(filter, predicate)
        filtered_partitions = self._pool.imap_unordered(filterer, partitions, self._chunksize)
        return itertools.chain.from_iterable(filtered_partitions)

    def aggregate(self, func, seed=default):
        partitions = realize_partitions(iter(self))
        if len(partitions) == 1 and len(partitions[0]) == 1:
            if seed is default:
                return partitions[0][0]
            else:
                return func(seed, partitions[0][0])
        reducer = functools.partial(functools.reduce, func)
        reduced_partitions = self._pool.map_unordered(reducer, partitions, self._chunksize)
        return ParallelQueryable(reduced_partitions).aggregate(func, seed)

    def as_ordered(self):
        return self._create_ordered(iter(self))

    def as_sequential(self):
        import queryable
        return queryable.Queryable(iter(self))

class OrderedParallelQueryable(ParallelQueryable):

    def __init__(self, iterable, func=None, pool=None, chunksize=1):
        super(OrderedParallelQueryable, self).__init__(iterable, pool, chunksize)
        self.funcs = [ func ] if func is not None else []

    def create(self, iterable):
        return OrderedParallelQueryable(iterable, self._pool, self._chunksize)

    def select(self, selector):
        '''Transforms each element of a sequence into a new form.

        Each element is transformed through a selector function to produce a value for each value in the source
        sequence. The generated sequence is lazily evaluated.

        Args:
            selector: A unary function mapping a value in the source sequence to the corresponding value in the generated
                generated sequence. The argument of the selector function
                (which can have any name) is,

                Args:
                    element: The value of the element

                Returns:
                    The selected value derived from the element value

        Returns:
            A generated sequence whose elements are the result of invoking the selector function on each element of the
            source sequence.
        '''
        return self.create(self._pool.imap(selector, iter(self), self._chunksize))

    def as_unordered(self):
        return self._create(iter(self))

    def then_by(self, func=identity):
        self.funcs.append(func)
        return self

    # TODO: then_by_descending

    def __iter__(self):
        partitions = realize_partitions(self._iter())
        # TODO: Ensure that the sort is stable
        # TODO: Try using functools.partial and respond to
        # http://techguyinmidtown.com/2009/01/23/hack-for-functoolspartial-and-multiprocessing/
        # Actually, maybe functools.partial is pickleable in Python 3
        # http://www.mail-archive.com/python-bugs-list@python.org/msg47732.html
        sorted_partitions = self._pool.map(sorter, zip(itertools.repeat(self.funcs), partitions), self._chunksize)
        return heapq.merge(*sorted_partitions)

def sorter(funcs_iterable):
    funcs, iterable = funcs_iterable
    decorated = [(tuple(func(item) for func in funcs), item) for item in iterable]
    decorated.sort()
    undecorated = [item for funcs, item in decorated]
    return undecorated

def realize_partitions(iterable, floor = 1, ceiling = 32768):
    '''Partition the input sequence into a list of lists'''
    return [list(part) for part in partition(iterable)]

def partition(iterable, floor = 1, ceiling = 32768):
    '''
    Partition an iterable into chunks.  Returns an iterator over partitions.
    '''
    partition_size = floor
    run_length = multiprocessing.cpu_count()
    count = 0
    run_count = 0

    try:
        while True:
            #print("partition_size =", partition_size)
            # Split the iterable and replace the original iterator to avoid advancing it
            partition, iterable = itertools.tee(iterable)

            # Yield the first partition, limited to the partition size
            yield Queryable(partition).take(partition_size)

            # Advance to the start of the next partition, this will raise StopIteration
            # if the iterator is exhausted
            for i in range(partition_size):
                next(iterable)

            # If we've reached the end of a run of this size, double the partition size
            run_count += 1
            if run_count >= run_length:
                partition_size *= 2
                run_count = 0

            # Unless we have hit the ceiling
            if partition_size > ceiling:
                partition_size = ceiling

    except StopIteration:
        pass

