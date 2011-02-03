'''
queryable.py A module for LINQ-like facility in Python.
'''

import heapq
import itertools
import functools
import sys

try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        sys.stderr.write('Could not import OrderedDict. For Python versions earlier than 2.7 install the')
        sys.stderr.write('ordereddict module from the Python Package Index with easy_install ordereddict.')
        sys.exit(1)

default = object()

def identity(x):
    '''The identity function.'''
    return x

def asq(iterable):
    '''Create a Queryable object from any iterable.

    Currently this factory only provides support for objects supporting the
    iterator protocol.  Future implementations may support other providers.

    Args:
        iterable: Any object supporting the iterator protocol.

    Returns:
        An instance of Queryable.
    '''
    return Queryable(iterable)

class Queryable(object):
    '''Queryable supports all of the chainable query methods implemented in a serial fashion,

    Queryable objects are constructed from iterables.
    '''

    def __init__(self, iterable):
        '''Construct a Queryable from any iterable.

        Args:
            iterable: Any object supporting the iterator protocol.
            
        Raises:
            ValueError: if iterable is None
            TypeError: if iterable does not support the iterator protocol.

        '''
        if iterable is None:
            raise ValueError("Cannot create Queryable from None type.")

        self._iterable = iterable

    def __iter__(self):
        '''Support for the iterator protocol.

        Allows Queryable instances to be used anywhere an iterable is required.

        Raises:
            ValueError: If the Queryable has been closed().
        '''
        if self.closed():
            raise ValueError("Attempt to use closed() Queryable")

        return self._iter()

    def _iter(self):
        '''Return an unsorted iterator over the iterable around which this Queryable has been constructed.

        Useful in subclasses to obtain a raw iterator over the iterable where __iter__ has been overridden.
        '''
        return iter(self._iterable)

    def _create(self, iterable):
        return Queryable(iterable)

    def _create_ordered(self, iterable, direction, func):
        return OrderedQueryable(iterable, direction, func)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        return False

    def closed(self):
        '''Determine whether the Queryable has been closed.

        Returns:
            True if closed, otherwise False.
        '''
        return self._iterable is None# and self._iterator is None

    def close(self):
        '''Closes the queryable.

        The Queryable should not be used following a call to close. This method is idempotent.
        '''
        self._iterable = None
        #self._iterator = None

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

        Raises:
            ValueError: If this Queryable has been closed.
            TypeError: If selector is not callable.
        '''
        if self.closed():
            raise ValueError("Attempt to call select() on a closed Queryable.")

        return self._create(map(selector, iter(self)))


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

        Raises:
            ValueError: If this Queryable has been closed.
            TypeError: If selector is not callable.
        '''
        if self.closed():
            raise ValueError("Attempt to call select_with_index() on a closed Queryable.")

        return self._create(itertools.starmap(selector, enumerate(iter(self))))

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

        Raises:
            ValueError: If this Queryable has been closed.
            TypeError: If projector [and selector] are not callable.
        '''
        if self.closed():
            raise ValueError("Attempt to call select_many() on a closed Queryable.")

        sequences = (self._create(item).select(projector) for item in iter(self))
        chained_sequence = itertools.chain.from_iterable(sequences)
        return self._create(map(selector, chained_sequence))
        
    def select_many_with_index(self, projector=lambda i,x:iter(x), selector=identity):
        '''Projects each element of a sequence to an intermediate new sequence, incorporating the index of the element,
        flattens the resulting sequence into one sequence and optionally transforms the flattened sequence using a
        selector function.

        Args:
            projector: A unary function mapping each element of the source sequence into an intermediate sequence. If no
                projection function is provided, the intermediate sequence will consist of the single corresponding
                element from the source sequence. The projector function argument (which can have any name) and return
                values are,

                Args:
                    index: The index of the element in the source sequence
                    element: The value of the element

                Returns:
                    An iterable derived from the element value

            selector: An optional unary function mapping the elements in the flattened intermediate sequence to
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

        Raises:
            ValueError: If this Queryable has been closed.
            TypeError: If projector [and selector] are not callable.
        '''
        if self.closed():
            raise ValueError("Attempt to call select_many_with_index() on a closed Queryable.")

        sequences = self.select_with_index(projector)
        chained_sequence = itertools.chain.from_iterable(sequences)
        return self._create(map(selector, chained_sequence))

    def select_many_with_correspondence(self, projector=iter, selector=lambda x, y: y):
        '''Projects each element of a sequence to an intermediate new sequence, and flattens the resulting sequence,
        into one sequence and uses a selector function to incorporate the corresponding source for each item in the
        result sequence.

        Args:
            projector: A unary function mapping each element of the source sequence into an intermediate sequence. If no
                projection function is provided, the intermediate sequence will consist of the single corresponding
                element from the source sequence. The projector function argument (which can have any name) and return
                values are,

                Args:    for item in self:
                intermediate_sequence = projector(item)
                for intermediate_item in intermediate_sequence:
                    yield selector(item, intermediate_item)
                    source_element: The value of the element

                Returns:
                    An iterable derived from the element value

            selector: An optional binary function mapping the elements in the flattened intermediate sequence to
                corresponding elements of the result sequence. If no selector function is provided, the identity
                function is used.  The selector function argument and return values are,

                Args:
                    source_element: The corresponding source element

                    element: The value of the intermediate element from the concatenated sequences arising from the
                        projector function.

                Returns:
                    The selected value derived from the element value

        Raises:
            ValueError: If this Queryable has been closed.
            TypeError: If projector or selector are not callable.
        '''

        if self.closed():
            raise ValueError("Attempt to call select_many_with_correspondence() on a closed Queryable.")

        return self._create(self._generate_select_many_with_correspondence(projector, selector))

    def _generate_select_many_with_correspondence(self, projector, selector):
        for item in self:
            intermediate_sequence = projector(item)
            for intermediate_item in intermediate_sequence:
                value = selector(item, intermediate_item)
                yield value

    def group_by(self, selector=identity):
        # TODO: Add missing parameters
        '''Groups the elements according to the value of a key extracted by a selector function.

        Note that this method has different behaviour to itertools.groupby in the Python standard library
        because it aggregates all items with the same key, rather than returning groups of consecutive
        items of the same key.

        Execution is deferred, but consumption of a single result will lead to evaluation of the whole source sequence.

        Args:
            selector: A unary function mapping a value in the source sequence to a key. The argument of the selector
                function (which can have any name) is,

                Args:
                    element: The value of the element

                Returns:
                    The selected value derived from the element value

        Returns:
            A Lookup containing Groupings.
        '''
        if self.closed():
            raise ValueError("Attempt to call select_with_index() on a closed Queryable.")

        # TODO: Defer execution somehow
        return self.to_lookup(selector)

    def where(self, predicate):
        return self._create(filter(predicate, iter(self)))

    def of_type(self, type):
        return self.where(lambda x: isinstance(x, type))

    def order_by(self, func=identity):
        return self._create_ordered(iter(self), -1, func)

    def order_by_descending(self, func=identity):
        return self._create_ordered(iter(self), +1, func)

    def take(self, n=1):
        return self._create(itertools.islice(self, n))

    def _generate_take(self, n):
        for index, item in enumerate(iter(self)):
            if index == n:
                break
            yield item

    def take_while(self, predicate):
        return self._create(itertools.takewhile(predicate, iter(self)))

    def skip(self, n=1):

        def skip_result():
            for index, item in enumerate(iter(self)):
                if index >= n:
                    yield item

        return self._create(skip_result())

    def skip_while(self, predicate):

        def skip_while_result():
            for item in iter(self):
                if not predicate(item):
                    yield item
                    break

        return self._create(skip_while_result())

    def concat(self, iterable):
        return self._create(itertools.chain(iter(self), iterable))

    def reverse(self):
        lst = list(iter(self))
        lst.reverse()
        return self._create(lst)

    def element_at(self, index):
        # Attempt to use __getitem__
        try:
            return self._iterable[index]
        except TypeError:
            pass

        # Fall back to iterating
        for i, item in enumerate(iter(self)):
            if i == index:
                return item
        raise IndexError("element_at(index) out of range.")
            

    def count(self):
        '''Return the number of elements in the iterable.

        Immediate execution.
        '''

        # Attempt to use len()
        try:
            return len(self._iterable)
        except TypeError:
            pass

        # Fall back to iterating
        index = -1

        for index, item in enumerate(iter(self)):
            pass

        return index + 1

    def any(self, predicate=identity):
        return any(self.select(predicate))

    def all(self, predicate=identity):
        return all(self.select(predicate))

    def min(self, func=identity):
        return min(self.select(func))

    def max(self, func=identity):
        return max(self.select(func))

    def sum(self, func=identity):
        return sum(self.select(func))

    def average(self, func=identity):
        total = 0
        for index, item in enumerate(iter(self)):
            total += func(item)
        return total / index

    def contains(self, value):
        # Test that this works with objects supporting only __contains__, __getitem__ and __iter__
        return value in self._iterable

    def default_if_empty(self, default):
        # Try to get an element from the iterator, if we succeed, the sequence
        # is non-empty. We store the extracted value in a generator and chain
        # it to the tail of the sequence in order to recreate the original
        # sequence.
        try:
            head = next(iter(self))

            def head_generator():
                yield head

            return self._create(itertools.chain(head_generator(), iter(self)))

        except StopIteration:
            # Return a sequence containing a single instance of the default val
            single = (default,)
            return self._create(single)

    def distinct(self, func=identity):

        def distinct_result():
            seen = set()
            for item in iter(self):
                t_item = func(item)
                if t_item in seen:
                    continue
                seen.add(t_item)
                yield item

        return self._create(distinct_result())

    def empty(self):
        return self._create(tuple())

    def difference(self, second_iterable, func=identity):

        def difference_result():
            second_set = set(func(x) for x in second_iterable)
            for item in iter(self):
                if func(item) in second_set:
                    continue
                yield item

        return self._create(difference_result())

    def intersect(self, second_iterable, func=identity):

        def intersect_result():
            second_set = set(func(x) for x in second_iterable)
            for item in iter(self):
                if func(item) in second_set:
                    yield item

        return self._create(intersect_result())

    def union(self, second_iterable, func=identity):
        return self._create(itertools.chain(iter(self), second_iterable)).distinct(func)

    def join(self, inner_iterable, outer_key_func=identity, inner_key_func=identity,
             result_func=lambda outer, inner: (outer, inner)):

        def join_result():
            for outer_item in iter(self):
                outer_key = outer_key_func(outer_item)
                for inner_item in inner_iterable:
                    inner_key = inner_key_func(inner_item)
                    if inner_key == outer_key:
                        yield result_func(outer_item, inner_item)

        return self._create(join_result())

    def first(self):
        return next(iter(self))

    def first_or_default(self, default):
        try:
            return next(iter(self))
        except StopIteration:
            return default

    def last(self):
        sentinel = object()
        result = sentinel

        for item in iter(self):
            result = item

        if item is sentinel:
            raise StopIteration()

        return item

    def last_or_default(self, default):
        sentinel = object()
        result = sentinel

        for item in iter(self):
            result = item

        if item is sentinel:
            return default

        return item

    def aggregate(self, func, seed=default):
        if seed is default:
            return functools.reduce(func, iter(self))
        return functools.reduce(func, iter(self), seed)

    @staticmethod
    def range(self, start, count):
        return self._create(range(start, start + count))

    @staticmethod
    def repeat(self, element, count):
        return self._create(itertools.repeat(element, count))

    def zip(self, second_iterable, func=lambda x,y: (x,y)):
        if self.closed():
            raise ValueError("Attempt to call zip() on a closed Queryable.")
        return self._create(self._generate_zip_result(second_iterable, func))

    def _generate_zip_result(self, second_iterable, func):
        second_iterator = iter(second_iterable)
        try:
            while True:
                x = next(iter(self))
                y = next(second_iterator)
                yield func(x, y)
        except StopIteration:
            pass

    def to_list(self):
        # Maybe use with closable(self) construct to achieve this.
        lst = list(self)
        # Ideally we would close here. Why can't we - what is the problem?
        #self.close()
        return lst

    def to_tuple(self):
        tup = tuple(self)
        # Ideally we would close here
        #self.close()
        return tup

    def to_lookup(self, selector=identity):
        '''Returns a MultiDict object, using the provided selector to generate a key for each item.

        Execution is immediate.
        '''
        key_value_pairs = self.select(lambda item: (selector(item), item))
        lookup = Lookup(key_value_pairs)
        # Ideally we would close here
        #self.close()
        return lookup


    def as_parallel(self, pool=None):
        from .parallel_queryable import ParallelQueryable
        return ParallelQueryable(self, pool)

    # Methods for more Pythonic usage

    # Note: __len__ cannot be efficiently implemented in an idempotent fashion (without consuming
    #       the iterable or changing the state of the object. Call count() instead.
    #       see http://stackoverflow.com/questions/3723337/listy-behavior-is-wrong-on-first-call
    #       for more details.
    #       This is problematic if a Queryable is realized using the list() constructor, which calls
    #       __len__ prior to constructing the list as an efficiency optimisation.

    def __contains__(self, item):
        return self.contains(item)

    def __getitem__(self, index):
        return self.element_at(index)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        # Must be careful not to consume the iterable here
        return 'Queryable({iterable})'.format(iterable=self._iterable)

class OrderedQueryable(Queryable):
    '''A Queryable representing an ordered iterable.

    The sorting implemented by this class in that a partial sort is performed so you don't pay
    for sorting results which are never enumerated.'''

    def __init__(self, iterable, order, func):
        '''Create an OrderedIterable.

            Args:
                iterable: The iterable sequence to be ordered
                order: +1 for ascending, -1 for descending
                func: The function to select the sorting key
        '''
        assert abs(order) == 1, 'order argument must be +1 or -1'
        super(OrderedQueryable, self).__init__(iterable)
        self._funcs = [ (order, func) ]

    def then_by(self, func=identity):
        self._funcs.append( (-1, func) )
        return self

    def then_by_descending(self, func=identity):
        self._funcs.append( (+1, func) )
        return self
        
    def __iter__(self):
        # A tuple subclass on which we will redefine the __lt__ operator
        # so we can use heapq for complex sorts
        class SortingTuple(tuple):
            pass
            
        # Determine which sorting algorithms to use
        directions = [direction for direction, _ in self._funcs]
        direction_total = sum(directions)
        if direction_total == -len(self._funcs):
            # Uniform ascending sort - do nothing
            pass
        elif direction_total == len(self._funcs):
            # Uniform descending sort - swap the comparison operators
            def less(lhs, rhs):
                return lhs > rhs
            SortingTuple.__lt__ = less
        else:
            # TODO: We could use some runtime code generation here to compile a custom
            #       comparison operator
            # Mixed ascending/descending sort

            def less(lhs, rhs):
                for direction, lhs_element, rhs_element in zip(directions, lhs, rhs):
                    cmp = (lhs_element > rhs_element) - (rhs_element > lhs_element)
                    if cmp == 0:
                        continue
                    if cmp == direction:
                        return True
                    if cmp == -direction:
                        return False
                return False
            SortingTuple.__lt__ = less

        # Uniform ascending sort - decorate, sort, undecorate using tuple element
        lst = [(SortingTuple(func(item) for _, func in self._funcs), item) for item in self._iterable]
        heapq.heapify(lst)
        while lst:
            key, item = heapq.heappop(lst)
            yield item

class Lookup(Queryable):
    '''A read-only ordered dictionary for which there can be multiple value for each key.'''

    def __init__(self, key_value_pairs):
        '''Construct with a sequence of (key, value) tuples.'''
        self._dict = OrderedDict()
        for key, value in key_value_pairs:
            if key not in self._dict:
                self._dict[key] = []
            self._dict[key].append(value)
        super(Lookup, self).__init__(Grouping(self._dict, key) for key in self._dict)

    def __getitem__(self, key):
        '''The sequence corresponding to a given key.'''
        return Grouping(self._dict, key)

    def __len__(self):
        '''The number of groupings (keys) in the lookup.'''
        return len(self._dict)

    def __contains__(self, key):
        return key in self._dict

    def __repr__(self):
        # TODO: Display in a format that would be consumable by the constructor
        return 'Lookup({d})'.format(d=self._dict)

    def apply_result_selector(self, selector=lambda key, sequence: sequence):
        return self._create(self._generate_apply_result_selector(selector))

    def _generate_apply_result_selector(self, selector):
        for grouping in self:
            yield selector(grouping.key, grouping)
        

class Grouping(Queryable):

    def __init__(self, ordereddict, key):
        self._key = key
        sequence = ordereddict[key]
        super(Grouping, self).__init__(sequence)

    key = property(lambda self: self._key)

    def __len__(self):
        return self.count()

    def __repr__(self):
        # TODO: Display in a format that would be consumable by the constructor
        return 'Grouping(key={k})'.format(k=self._key)

# TODO: Should we use a class factory to generate the parallel equivalents of these?







