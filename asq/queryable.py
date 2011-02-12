'''
queryable.py A module for LINQ-like facility in Python.
'''

import heapq
import itertools
import operator

from .portability import (imap, ifilter, irange, izip, izip_longest, fold, OrderedDict)

default = object()

def identity(x):
    '''The identity function.'''
    return x

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False
        
def asq(iterable):
    '''Create a Queryable object from any iterable.

    Currently this factory only provides support for objects supporting the
    iterator protocol.  Future implementations may support other providers.

    Args:
        iterable: Any object supporting the iterator protocol.

    Returns:
        An instance of Queryable.

    Raises:
        TypeError: If iterable is not actually iterable
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
            TypeError: if iterable does not support the iterator protocol.

        '''
        if not is_iterable(iterable):
            raise TypeError("Cannot construct Queryable from non-iterable {type}".format(type=str(type(iterable))[7: -2]))

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

        if selector is identity:
            return self

        return self._create(imap(selector, self))


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
            raise ValueError("Attempt to call select_many() on a closed Queryable.")

        sequences = self.select(projector)
        chained_sequence = itertools.chain.from_iterable(sequences)
        return self._create(chained_sequence).select(selector)
        
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
        return self._create(imap(selector, chained_sequence))

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
                # Use select() here too?
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
            A sequence of Groupings.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call select_with_index() on a closed Queryable.")

        return self._create(self._generate_group_by_result(selector))

    def _generate_group_by_result(self, selector):
        lookup = self.to_lookup(selector)
        for grouping in lookup:
            yield grouping

    def where(self, predicate):
        if self.closed():
            raise ValueError("Attempt to call where() on a closed Queryable.")

        return self._create(ifilter(predicate, self))

    def of_type(self, type):
        if self.closed():
            raise ValueError("Attempt to call of_type() on a closed Queryable.")

        return self.where(lambda x: isinstance(x, type))

    def order_by(self, func=identity):
        if self.closed():
            raise ValueError("Attempt to call order_by() on a closed Queryable.")

        return self._create_ordered(iter(self), -1, func)

    def order_by_descending(self, func=identity):
        if self.closed():
            raise ValueError("Attempt to call order_by_descending() on a closed Queryable.")

        return self._create_ordered(iter(self), +1, func)

    def take(self, count=1):
        '''Returns a specified number of contiguous elements from the start of a sequence.

        If the source sequence contains fewer elements than requested only the available
        elements will be returned and no exception will be raised.

        Args:
            count: The number of elements to take.

        Returns:
            The first count elements of the source sequence, or the number of elements in
            the source, whichever is greater.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call take() on a closed Queryable.")

        count = max(0, count)

        return self._create(itertools.islice(self, count))

    def take_while(self, predicate):
        '''Returns a contiguous sequence of elements from the source sequence for which
        the supplied predicate is True.

        Args:
            predicate: A function returning True or False with which elements will be tested.

        Returns:
            The elements from the beginning of the source sequence for which predicate is True.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call take_while() on a closed Queryable.")

        # Cannot use itertools.takewhile here because it is not lazy
        #return self._create(itertools.takewhile(predicate, self))

        return self._create(self._generate_take_while_result(predicate))

    def _generate_take_while_result(self, predicate):
        for x in self:
            if predicate(x):
                yield x
            else:
                break

    def skip(self, count=1):
        '''Skip the first count contiguous elements of the source sequence.

        If the source sequence contains fewer than count elements returns an empty sequence
        and does not raise an exception.

        Args:
            count: The number of elements to skip from the beginning of the sequence. If omitted
                defaults to one.

        Returns:
            The elements of source excluding the first count elements.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call skip() on a closed Queryable.")

        count = max(0, count)

        if count == 0:
            return self

        # Try an optimised version
        if hasattr(self._iterable, "__getitem__"):
            try:
                stop = len(self._iterable)
                return self._create(self._generate_optimized_skip_result(count, stop))
            except TypeError:
                pass

        # Fall back to the unoptimized version
        return self._create(self._generate_skip_result(count))

    def _generate_optimized_skip_result(self, count, stop):
        for i in irange(count, stop):
            yield self._iterable[i]

    def _generate_skip_result(self, count):
        for i, item in enumerate(self):
            if i < count:
                continue
            yield item

    def skip_while(self, predicate):
        '''Omit a contiguous sequence of elements from the beginning of the source sequence
        which match a predicate.

        Args:
            predicate: A single argument predicate function.

        Returns:
            The sequence of elements beginning with the first element for which the predicate
            returns False.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call take_while() on a closed Queryable.")

        return self._create(itertools.dropwhile(predicate, self))
        
    def concat(self, iterable):
        if self.closed():
            raise ValueError("Attempt to call concat() on a closed Queryable.")

        return self._create(itertools.chain(self, iterable))

    def reverse(self):
        '''Returns the sequence reversed.

        Execution is deferred, but the whole source sequence is consumed once execution commences.

        Returns:
            The source sequence in reverse order.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call reverse() on a closed Queryable.")

        # Attempt an optimised version
        try:
            r = reversed(self._iterable)
            return self._create(r)
        except TypeError:
            pass

        # Fall through to a sequential version
        return self._create(self._generate_reverse_result())

    def _generate_reverse_result(self):
        lst = list(iter(self))
        lst.reverse()
        for item in lst:
            yield item

    def element_at(self, index):
        '''Return the element at ordinal index.

        This method is evaluated immediately.

        Args:
            index: The index of the element to be returned.

        Returns:
            The element at ordinal index in the source sequence.

        Raises:
            ValueError: If the Queryable is closed()
            ValueError: If index is out of range.
        '''
        if self.closed():
            raise ValueError("Attempt to call element_at() on a closed Queryable.")

        if index < 0:
            raise ValueError("Attempt to use negative index")

        # Attempt to use __getitem__
        try:
            return self._iterable[index]
        except IndexError:
            raise ValueError("Index out of range")
        except TypeError:
            pass

        # Fall back to iterating
        for i, item in enumerate(self):
            if i == index:
                return item
        raise IndexError("element_at(index) out of range.")
            

    def count(self):
        '''Return the number of elements in the iterable.

        This method is evaluated immediately.
        '''

        if self.closed():
            raise ValueError("Attempt to call element_at() on a closed Queryable.")

        # Attempt to use len()
        try:
            return len(self._iterable)
        except TypeError:
            pass

        # Fall back to iterating
        index = -1

        for index, item in enumerate(self):
            pass

        return index + 1

    def any(self, predicate=None):
        '''Determine if the source sequence contains any elements which satisfy the predicate.

        Only enough of the sequence to satisfy the predicate once is consumed. Execution is immediate.

        Args:
            predicate: An optional single argument function used to test each element. If omitted,
                or None, this method returns True if their is at least one element in the source.

        Returns:
            True if the sequence contains at least one element which satisfies the predicate,
                otherwise False.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call any() on a closed Queryable.")

        if predicate is None:
            predicate = lambda x: True
            
        for item in self.select(predicate):
            if item:
                return True
        return False

    def all(self, predicate=identity):
        '''Determine if all elements in the source sequence satisfy a condition.

        All of the source sequence will be consumed. Execution is imediate.

        Args:
            predicate: An optional single argument function used to test each elements. If omitted,
                the identity function is used resulting in the elements being tested directly.

        Returns:
            True if all elements in the sequence meet the predicate condition, otherwise False.

        Raises:
            ValueError: If the Queryable is closed()
        '''
        if self.closed():
            raise ValueError("Attempt to call all() on a closed Queryable.")

        return all(self.select(predicate))

    def min(self, selector=identity):
        '''Return the minimum value in a sequence.

        All of the source sequence will be consumed. Execution is immediate.

        Args:
            selector: An optional single argument function which will be used to project
                the elements of the sequence. If omitted, the identity function is used.

        Returns:
            The minimum value of the projected sequence.

        Raises:
            ValueError: If the Queryable has been closed.
            ValueError: If the sequence is empty.
        '''
        if self.closed():
            raise ValueError("Attempt to call min() on a closed Queryable.")

        return min(self.select(selector))

    def max(self, func=identity):
        '''Return the maximum value in a sequence.

        All of the source sequence will be consumed. Execution is immediate.

        Args:
            selector: An optional single argument function which will be used to project
                the elements of the sequence. If omitted, the identity function is used.

        Returns:
            The maximum value of the projected sequence.

        Raises:
            ValueError: If the Queryable has been closed.
            ValueError: If the sequence is empty.
        '''

        if self.closed():
            raise ValueError("Attempt to call max() on a closed Queryable.")

        return max(self.select(func))

    def sum(self, func=identity):
        '''Return the arithmetic sum of the values in the sequence..

        All of the source sequence will be consumed. Execution is immediate.

        Args:
            selector: An optional single argument function which will be used to project
                the elements of the sequence. If omitted, the identity function is used.

        Returns:
            The total value of the projected sequence, or zero for an empty sequence.

        Raises:
            ValueError: If the Queryable has been closed.
        '''

        if self.closed():
            raise ValueError("Attempt to call sum() on a closed Queryable.")

        return sum(self.select(func))

    def average(self, func=identity):
        '''Return the arithmetic mean of the values in the sequence..

        All of the source sequence will be consumed. Execution is immediate.

        Args:
            selector: An optional single argument function which will be used to project
                the elements of the sequence. If omitted, the identity function is used.

        Returns:
            The mean value of the projected sequence.

        Raises:
            ValueError: If the Queryable has been closed.
            ValueError: I the source sequence is empty.
        '''
        if self.closed():
            raise ValueError("Attempt to call average() on a closed Queryable.")

        total = 0
        count = 0
        for item in self.select(func):
            total += item
            count += 1
        if count == 0:
            raise ValueError("Cannot compute average() of an empty sequence.")
        return total / count

    def contains(self, value):
        '''Determines whether the sequence contains a particular value.

        Execution is immediate. Depending on the type of the sequence, all or none of the
        sequence may be consumed by this operation.

        Args:
            value: The value to test for membership of the sequence

        Returns:
            True if value is in the sequence, otherwise False.

        Raises:
            ValueError: If the Queryable has been closed.

        '''
        if self.closed():
            raise ValueError("Attempt to call contains() on a closed Queryable.")

        # Test that this works with objects supporting only __contains__, __getitem__ and __iter__
        return value in self._iterable

    def default_if_empty(self, default):
        '''If the source sequence is empty return a single element sequence containing the
        supplied default value, otherwise return the source sequence unchanged.

        Args:
            default: The element to be returned if the source sequence is empty.

        Returns:
            The source sequence, or if the source sequence is empty an sequence containing a
            single element with the supplied default value.
        '''

        if self.closed():
            raise ValueError("Attempt to call default_if_empty() on a closed Queryable.")

        # Try to get an element from the iterator, if we succeed, the sequence
        # is non-empty. We store the extracted value in a generator and chain
        # it to the tail of the sequence in order to recreate the original
        # sequence.
        try:
            items = iter(self)
            head = next(items)

            def head_generator():
                yield head

            return self._create(itertools.chain(head_generator(), items))

        except StopIteration:
            # Return a sequence containing a single instance of the default val
            single = (default,)
            return self._create(single)

    def distinct(self, selector=identity):
        '''Eliminate duplicate elements from a sequence.

        Args:
            selector: An optional single argument function the result of which is the value compared for
                uniqueness against elements already consumed. If omitted, the element value itself
                is compared for uniqueness.

        Returns:
            Unique elements of the source sequence as determined by the selector function.  Note
            that t is unprojected elements that are returned, even if a selector was provided.

        Raises:
            ValueError: If the Queryable is closed.
        '''
        if self.closed():
            raise ValueError("Attempt to call distinct() on a closed Queryable.")

        return self._create(self._generate_distinct_result(selector))

    def _generate_distinct_result(self, selector):
        seen = set()
        for item in self:
            t_item = selector(item)
            if t_item in seen:
                continue
            seen.add(t_item)
            yield item

    @staticmethod
    def empty():
        '''Returns an empty queryable.

        The same empty instance will be returned each time.
        '''
        return _empty

    def difference(self, second_iterable, selector=identity):
        '''Returns those elements which are in the source sequence which are not in the
        second_iterable.

        This method is equivalent to the Except() LINQ operator, renamed to a valid
        Python identifier.

        Execution is deferred, but as soon as execution commences the entirety of the second_iterable
        is consumed; therefore, although the source sequence may be infinite the second_iterable must be finite.

        Args:
            second_iterable: Elements from this sequence are excluded from the returned sequence. This sequence
                will be consumed in its entirety, so must be finite.

            selector: An optional single argument function which is used to project the elements
                in the source and second_iterables prior to comparing them.

        Returns:
            A sequence containing all elements in the source sequence except those which are also members of the second
            sequence.

        Raises:
            ValueError: If the Queryable has been closed.
            ValueError: If the second_iterable is None
        '''
        if self.closed():
            raise ValueError("Attempt to call difference() on a closed Queryable.")

        if not is_iterable(second_iterable):
            raise TypeError("Cannot compute difference() with second_iterable of non-iterable {type}".format(
                    type=str(type(second_iterable))[7: -2]))

        return self._create(self._generate_difference_result(second_iterable, selector))

    def _generate_difference_result(self, second_iterable, selector):
        seen_elements = self._create(second_iterable).select(selector).distinct().to_set()
        for item in self:
            sitem = selector(item)
            if selector(item) not in seen_elements:
                seen_elements.add(sitem)
                yield item

    def intersect(self, second_iterable, selector=identity):
        '''Returns those elements which are both in the source sequence and in the
        second_iterable.

        Execution is deferred.

        Args:
            second_iterable: Elements are returned if they are also in the sequence.

            selector: An optional single argument function which is used to project the elements
                in the source and second_iterables prior to comparing them.

        Returns:
            A sequence containing all elements in the source sequence  which are also members of the second
            sequence.

        Raises:
            ValueError: If the Queryable has been closed.
            TypeError: If the second_iterable is not in fact iterable
        '''
        if self.closed():
            raise ValueError("Attempt to call intersect() on a closed Queryable.")

        if not is_iterable(second_iterable):
            raise TypeError("Cannot compute intersect() with second_iterable of non-iterable {type}".format(
                    type=str(type(second_iterable))[7: -1]))

        return self._create(self._generate_intersect_result(second_iterable, selector))

    def _generate_intersect_result(self, second_iterable, selector):
        second_set = self._create(second_iterable).select(selector).distinct().to_set()
        for item in self:
            sitem = selector(item)
            if sitem in second_set:
                second_set.remove(sitem)
                yield item

    def union(self, second_iterable, selector=identity):
        '''Returns those elements which are either in the source sequence or in the
        second_iterable.

        Execution is deferred.

        Args:
            second_iterable: Elements from this sequence are returns if they are not also in the source sequence.

            selector: An optional single argument function which is used to project the elements
                in the source and second_iterables prior to comparing them.

        Returns:
            A sequence containing all elements in the source sequence and second sequence.

        Raises:
            ValueError: If the Queryable has been closed.
            ValueError: If the second_iterable is None
        '''
        if self.closed():
            raise ValueError("Attempt to call union() on a closed Queryable.")

        if not is_iterable(second_iterable):
            raise TypeError("Cannot compute union() with second_iterable of non-iterable {type}".format(
                    type=str(type(second_iterable))[7: -1]))

        return self._create(itertools.chain(self, second_iterable)).distinct(selector)

    def join(self, inner_iterable, outer_key_selector=identity, inner_key_selector=identity,
             result_selector=lambda outer, inner: (outer, inner)):

        if self.closed():
            raise ValueError("Attempt to call join() on a closed Queryable.")

        if not is_iterable(inner_iterable):
            raise TypeError("Cannot compute join() with inner_iterable of non-iterable {type}".format(
                    type=str(type(inner_iterable))[7: -1]))

        return self._create(self._generate_join_result(inner_iterable, outer_key_selector,
                                                       inner_key_selector, result_selector))

    def _generate_join_result(self, inner_iterable, outer_key_selector, inner_key_selector, result_selector):
        lookup = self._create(inner_iterable).to_lookup(inner_key_selector)
        result = self.select_many_with_correspondence(lambda outer_element: lookup[outer_key_selector(outer_element)],
                                                      result_selector)
        for item in result:
            yield item

    def group_join(self, inner_iterable, outer_key_selector=identity, inner_key_selector=identity,
             result_selector=lambda outer, inner: (outer, inner)):

        if self.closed():
            raise ValueError("Attempt to call group_join() on a closed Queryable.")

        if not is_iterable(inner_iterable):
            raise TypeError("Cannot compute group_join() with inner_iterable of non-iterable {type}".format(
                    type=str(type(inner_iterable))[7: -1]))

        return self._create(self._generate_group_join_result(inner_iterable, outer_key_selector,
                                                       inner_key_selector, result_selector))

    def _generate_group_join_result(self, inner_iterable, outer_key_selector, inner_key_selector, result_selector):
        lookup = self._create(inner_iterable).to_lookup(inner_key_selector)
        for outer_element in self:
            outer_key = outer_key_selector(outer_element)
            yield result_selector(outer_element, lookup[outer_key])

    def first(self, predicate=None):
        if self.closed():
            raise ValueError("Attempt to call first() on a closed Queryable.")

        return self._first() if predicate is None else self._first_predicate(predicate)

    def _first(self):
        try:
            return next(iter(self))
        except StopIteration:
            raise ValueError("Cannot return first() from an empty sequence.")

    def _first_predicate(self, predicate):
        for item in self:
            if predicate(item):
                return item
        raise ValueError("No elements matching predicate in call to first()")

    def first_or_default(self, default, predicate=None):
        if self.closed():
            raise ValueError("Attempt to call first_or_default() on a closed Queryable.")

        return self._first_or_default(default) if predicate is None else self._first_or_default_predicate(default, predicate)

    def _first_or_default(self, default):
        try:
            return next(iter(self))
        except StopIteration:
            return default

    def _first_or_default_predicate(self, default, predicate):
        for item in self:
            if predicate(item):
                return item
        return default
    
    def single(self, predicate=None):
        if self.closed():
            raise ValueError("Attempt to call single() on a closed Queryable.")

        return self._single() if predicate is None else self._single_predicate(predicate)

    def _single(self):
        p = iter(self)

        try:
            result = next(p)
        except StopIteration:
            raise ValueError("Cannot return single() from an empty sequence.")

        try:
            next(p)
        except StopIteration:
            return result

        raise ValueError("Sequence for single() contains multiple elements")
    
    def _single_predicate(self, predicate):
        found = False
        for item in self:
            if predicate(item):
                if found == True:
                    raise ValueError("Sequence contains more than one value matching singe() predicate")
                result = item
                found = True
        if found == False:
            raise ValueError("Sequence for single() contains no items matching the predicate")
        return result

    def single_or_default(self, default, predicate=None):
        if self.closed():
            raise ValueError("Attempt to call single() on a closed Queryable.")

        return self._single_or_default(default) if predicate is None else self._single_or_default_predicate(default, predicate)

    def _single_or_default(self, default):
        p = iter(self)

        try:
            result = next(p)
        except StopIteration:
            return default

        try:
            next(p)
        except StopIteration:
            return result

        raise ValueError("Sequence for single() contains multiple elements")


    def _single_or_default_predicate(self, default, predicate):
        found = False
        result = default
        for item in self:
            if predicate(item):
                if found == True:
                    raise ValueError("Sequence contains more than one value matching singe() predicate")
                result = item
                found = True
        return result


    def last(self, predicate=None):
        if self.closed():
            raise ValueError("Attempt to call last() on a closed Queryable.")

        return self._last() if predicate is None else self._last_predicate(predicate)

    def _last(self):
        # Attempt an optimised version
        try:
            count = len(self._iterable)
            return self._iterable[count - 1]
        except:
            pass

        sentinel = object()
        result = sentinel

        for item in self:
            result = item

        if result is sentinel:
            raise ValueError("Cannot return last() from an empty sequence.")

        return result

    def _last_predicate(self, predicate):
        # Attempt an optimised version
        try:
            r = reversed(self._iterable)
            self._create(r).first(predicate)
        except TypeError:
            pass

        # Fall through to the sequential version
        sentinel = object()
        result = sentinel

        for item in self:
            if predicate(item):
                result = item

        if result is sentinel:
            raise ValueError("No item matching predicate in call to last()")

        return result


    def last_or_default(self, default, predicate=None):
        if self.closed():
            raise ValueError("Attempt to call last_or_default() on a closed Queryable.")

        return self._last_or_default(default) if predicate is None else self._last_or_default_predicate(default, predicate)

    def _last_or_default(self, default):
        # Attempt an optimised version
        try:
            count = len(self._iterable)
            if count == 0:
                return default
            return self._iterable[count - 1]
        except:
            pass

        # Fall through to the sequential version
        sentinel = object()
        result = sentinel

        for item in iter(self):
            result = item

        if result is sentinel:
            return default

        return result

    def _last_or_default_predicate(self, default, predicate):
        try:
            r = reversed(self._iterable)
            return self._create(r).first_or_default(default, predicate)
        except TypeError:
            # Fall through to the sequential version
            pass
        
        sentinel = object()
        result = sentinel

        for item in iter(self):
            if predicate(item):
                result = item

        if result is sentinel:
            return default

        return result


    def aggregate(self, func, seed=default, result_selector=identity):
        '''
        Raises:
            ValueError: If called on an empty sequence with no seed value.
        '''
        if self.closed():
            raise ValueError("Attempt to call aggregate() on a closed Queryable.")

        if seed is default:
            try:
                return result_selector(fold(func, self))
            except TypeError as e:
                if 'empty sequence' in str(e):
                    raise ValueError("Cannot aggregate() empty sequence with no seed value")
        return result_selector(fold(func, self, seed))

    @classmethod
    def range(cls, start, count):
        if count < 0:
            raise ValueError("range() count cannot be negative")
        return cls(irange(start, start + count))

    @classmethod
    def repeat(cls, element, count):
        if count < 0:
            raise ValueError("repeat() count cannot be negative")
        return cls(itertools.repeat(element, count))

    def zip(self, second_iterable, func=lambda x,y: (x,y)):
        if self.closed():
            raise ValueError("Attempt to call zip() on a closed Queryable.")
        return self._create(func(*t) for t in izip(self, second_iterable))

    def to_list(self):
        # Maybe use with closable(self) construct to achieve this.
        if isinstance(self._iterable, list):
            return self._iterable
        lst = list(self)
        # Ideally we would close here. Why can't we - what is the problem?
        #self.close()
        return lst

    def to_tuple(self):
        if isinstance(self._iterable, tuple):
            return self._iterable
        tup = tuple(self)
        # Ideally we would close here
        #self.close()
        return tup

    def to_set(self):
        '''Build a dictionary from the source sequence.

        Raises:
            ValueError: If duplicate keys are in the projected source sequence.
            ValueError: If the Queryable is closed()
        '''

        if isinstance(self._iterable, set):
            return self._iterable
        s = set()
        for item in self:
            if item in s:
                raise ValueError("Duplicate item value {item} in sequence during to_dictionary()".format(item=repr(item)))
            s.add(item)
        # Ideally we would close here
        #self.close()
        return s

    def to_lookup(self, key_selector=identity, value_selector=identity):
        '''Returns a Lookup object, using the provided selector to generate a key for each item.

        Execution is immediate.
        '''
        key_value_pairs = self.select(lambda item: (key_selector(item), value_selector(item)))
        lookup = Lookup(key_value_pairs)
        # Ideally we would close here
        #self.close()
        return lookup

    def to_dictionary(self, key_selector=identity, value_selector=identity):
        '''Build a dictionary from the source sequence.

        Raises:
            ValueError: If duplicate keys are in the projected source sequence.
        '''
        dictionary = {}
        for key, value in self.select(lambda x: (key_selector(x), value_selector(x))):
            if key in dictionary:
                raise ValueError("Duplicate key value {key} in sequence during to_dictionary()".format(key=repr(key)))
            dictionary[key] = value
        return dictionary

    def sequence_equal(self, second_iterable, equality_comparer=operator.eq):
        if not is_iterable(second_iterable):
            raise TypeError("Cannot compute sequence_equal() with second_iterable of non-iterable {type}".format(
                    type=str(type(second_iterable))[7: -1]))

        # Try to check the lengths directly as an optimization
        try:
            if len(self._iterable) != len(second_iterable):
                return False
        except TypeError:
            pass

        sentinel = object()
        for first, second in izip_longest(self, second_iterable, fillvalue=sentinel):
            if first is sentinel or second is sentinel:
                return False
            if not equality_comparer(first, second):
                return False
        return True

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

    # TODO: def __reversed__(self):


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
        '''The sequence corresponding to a given key, or an empty sequence if
           there are no values corresponding to that key.

        Args:
            key: The key of the group to be returned.

        Returns:
            The Grouping corresponding to the supplied key.
        '''
        return Grouping(self._dict, key)

    def __len__(self):
        '''The number of groupings (keys) in the lookup.'''
        return len(self._dict)

    def __contains__(self, key):
        return key in self._dict

    def __repr__(self):
        return 'Lookup({d})'.format(d=list(self._generate_repr_result()))

    def _generate_repr_result(self):
        for key in self._dict:
            for value in self._dict[key]:
                yield (key, value)

    def apply_result_selector(self, selector=lambda key, sequence: sequence):
        return self._create(self._generate_apply_result_selector(selector))

    def _generate_apply_result_selector(self, selector):
        for grouping in self:
            yield selector(grouping.key, grouping)

class Grouping(Queryable):

    def __init__(self, ordereddict, key):
        self._key = key
        sequence = ordereddict[key] if key in ordereddict else self.empty()
        super(Grouping, self).__init__(sequence)

    key = property(lambda self: self._key)

    def __len__(self):
        return self.count()

    def __repr__(self):
        # TODO: Display in a format that would be consumable by the constructor
        return 'Grouping(key={k})'.format(k=repr(self._key))

# TODO: Should we use a class factory to generate the parallel equivalents of these?

_empty = Queryable(tuple())
