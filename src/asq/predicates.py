'''Predicate function factories'''

__author__ = 'Sixty North'


def eq_(rhs):
    '''Create a predicate which tests its argument for equality with a value.

    Args:
        rhs: (right-hand-side) The value with which the left-hand-side element
            will be compared for equality.

    Returns:
        A unary predicate function which compares its single argument (lhs)
        for equality with rhs.
    '''
    return lambda lhs: lhs == rhs


def ne_(rhs):
    '''Create a predicate which tests its argument for inequality with a value.

    Args:
        rhs: (right-hand-side) The value with which the left-hand-side element
            will be compared for inequality.

    Returns:
        A unary predicate function which compares its single argument (lhs)
        for inequality with rhs.
    '''
    return lambda lhs: lhs != rhs


def lt_(rhs):
    '''Create a predicate which performs a less-than comparison of its argument
    with a value.

    Args:
        rhs: (right-hand-side) The value against which the less-than test will
            be performed.

    Returns:
        A unary predicate function which determines whether its single
        argument (lhs) is less-than rhs.
    '''
    return lambda lhs: lhs < rhs


def le_(rhs):
    '''Create a predicate which performs a less-than-or-equal comparison of its
    argument with a value.

    Args:
        rhs: (right-hand-side) The value against which the less-than-or-equal
            test will be performed.

    Returns:
        A unary predicate function which determines whether its single
        argument (lhs) is less-than-or-equal to rhs.
    '''
    return lambda lhs: lhs <= rhs


def ge_(rhs):
    '''Create a predicate which performs a greater-than-or-equal comparison of
    its argument with a value.

    Args:
        rhs: (right-hand-side) The value against which the greater-than-or-
            equal test will be performed.

    Returns:
        A unary predicate function which determines whether its single
        argument (lhs) is greater-than rhs.
    '''
    return lambda lhs: lhs >= rhs


def gt_(rhs):
    '''Create a predicate which performs a greater-than comparison of its
    argument with a value.

    Args:
        rhs: (right-hand-side) The value against which the greater-than test
            will be performed.

    Returns:
        A unary predicate function which determines whether its single
        argument (lhs) is less-than-or-equal to rhs.
    '''
    return lambda lhs: lhs > rhs


def is_(rhs):
    '''Create a predicate which performs an identity comparison of its
    argument with a value.

    Args:
        rhs: (right-hand-side) The value against which the identity test will
            be performed.

    Returns:
        A unary predicate function which determines whether its single
        arguments (lhs) has the same identity - that is, is the same object -
        as rhs.
    '''
    return lambda lhs: lhs is rhs


def contains_(lhs):
    '''Create a unary predicate which tests for membership if its argument.

    Args:
        lhs: (left-hand-side) The value to test for membership for in the
            predicate argument.

    Returns:
        A unary predicate function which determines whether its single
        arguments (lhs) contains lhs.
    '''
    return lambda rhs: lhs in rhs


def not_(predicate):
    '''A predicate combinator which negates produces an inverted predicate.

    The predicate returned by this combinator is the logical inverse of the
    supplied combinator.

    Args:
        predicate: A unary predicate function to be inverted.

    Returns:
        A unary predicate function which is the logical inverse of pred.
    '''
    return lambda lhs: not predicate(lhs)


def and_(predicate1, predicate2):
    '''A predicate combinator which produces the a new predicate which is the
    logical conjunction of two existing unary predicates.

    The predicate returned by this combinator returns True when both of the two
    supplied predicates return True, otherwise it returns False.

    Args:
        predicate1: A unary predicate function.
        predicate2: A unary predicate function.

    Returns:
        A unary predicate function which is the logical conjunction of
        predicate1 and predicate2.
    '''
    return lambda lhs: predicate1(lhs) and predicate2(lhs)


def or_(predicate1, predicate2):
    '''A predicate combinator which produces the a new predicate which is the
    logical disjunction of two existing unary predicates.

    The predicate returned by this combinator returns True when either or both
    of the two supplied predicates return True, otherwise it returns False.

    Args:
        predicate1: A unary predicate function.
        predicate2: A unary predicate function.

    Returns:
        A unary predicate function which is the logical disjunction of
        predicate1 and predicate2.
    '''
    return lambda lhs: predicate1(lhs) or predicate2(lhs)


def xor_(predicate1, predicate2):
    '''A predicate combinator which produces the a new predicate which is the
    logical exclusive disjunction of two existing unary predicates.

    The predicate returned by this combinator returns True when the two
    supplied predicates return the different values, otherwise it returns
    False.

    Args:
        predicate1: A unary predicate function.
        predicate2: A unary predicate function.

    Returns:
        A unary predicate function which is the logical exclusive disjunction
        of predicate1 and predicate2.
    '''
    return lambda lhs: predicate1(lhs) != predicate2(lhs)
