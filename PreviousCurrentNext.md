An operator equivalent to this:

```
def adjacent(seq, pad=None):
    '''
    Returns a slicing window of width 3 over date from the iterable, padded with an given value.

    s -> (None, s0, s1), (s1, s2, s3), (sn-1, sn, None)

    '''
    padded = itertools.chain((pad,), seq, (pad,))
    previous_iter, current_iter, next_iter = itertools.tee(padded, 3)
    next(current_iter)
    next(next_iter); next(next_iter)
    return itertools.izip(previous_iter, current_iter, next_iter)
```

but with better error checking for short sequences.