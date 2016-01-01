__author__ = 'Sixty North'


def insensitive_eq(lhs, rhs):
    '''Case insensitive string equality operator.

    Args:
        lhs (str): The first string to be compared.
        rhs (str): The second string to be compared.

    Returns:
        True if the strings are equal in a case insensitive way, otherwise
        False.
    '''
    return lhs.lower() == rhs.lower()
