# drop\_last #

```
import asq.extension
import asq.queryables
import asq.initiators

from collections import deque

# Add a new query operator to asq
@asq.extension.extend(asq.queryables.Queryable)
def drop_last(self, count=1):
    '''Drop the last count items of sequence.
    
    Note: This method uses deferred execution.
    
    Args:
        self: The Queryable sequence.
        
        count: The number of items to be dropped from th eend of the sequence.
        
    Returns:
        A Queryable over the shortened sequence.
    '''
    # Validate the arguments
    if self.closed():
        raise ValueError("Attempt to call drop_last() on a closed Queryable.")
    
    if count < 0:
        raise ValueError("drop_last() : count should be non-negative.")

    # Define a generator to support deferred execution (lazy evaluation) we need
    # to define a generator. This generator is also a closure over the
    # parameters to separate_with, namely 'self' and 'separator'.
    def generator():
        
        buf = deque(maxlen = count + 1)
        
        for item in self:
            buf.append(item)
            if len(buf) == count + 1:
                yield buf.popleft()
    
    return self._create(generator())
    
if __name__ == '__main__':
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print asq.initiators.query(a).drop_last(3).to_list()

```