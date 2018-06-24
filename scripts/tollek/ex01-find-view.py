import numpy as np

def find_index(base, view):
    """
    Given an array that is `view` of `bave`, find an index sich that
    base[index] is view`

    Assumes both base and view has the same itemsize??
    """

    if not isinstance(view, np.ndarray):
        return "..."

    itemsize = view.itemsize
    offset_start = (np.byte_bounds(view)[0] - np.byte_bounds(base)[0]) // itemsize
    # without the -1, we'd be pointing to first element not beginning to the view (exclusive). We want inclusive.
    offset_end = (np.byte_bounds(view)[-1] - np.byte_bounds(base)[-1] - 1) // itemsize

    index_start = np.unravel_index(offset_start, base.shape)
    index_stop = np.unravel_index((offset_end + base.size) % base.size, base.shape)
    index_step = np.array(view.strides) // np.array(base.strides)

    index = ""
    for i in range(len(index_step)):
        start = index_start[i]
        stop = index_stop[i]
        step = index_step[i]

        if start == stop:
            # Z[3:4] = '3' -> no need for stop or step
            stop, step = None, None
        else:
            if start == 0:
                start = None
            if stop == base.shape[i] - 1:
                stop = None
        if step is not None and stop is not None:
            if step > 0:
                start, stop = start, stop + 1
            else:
                start, stop = stop, start - 1 

        # format the index properly
        if start is not None:
            index += str(start)
        if stop is not None:
            index += ":" + str(stop)
        elif step is not None:  # placeholder for "::2"
            index += ":"
        if step is not None:
            index += ":" + str(step)
        index += ","
    index = index[:-1]
    return index

def debug_print(s):
    # print(s)
    pass

def test_find_index():
    base = np.arange(8 * 8).reshape(8, 8)
    # Sub-array
    Z = base[1:-1,1:-1]
    index = find_index(base,Z)
    debug_print(index)
    print(np.allclose(Z, eval("base[%s]" % index)))
    
    # Every two items
    Z = base[::2,::2]
    index = find_index(base,Z)
    debug_print(index)
    print(np.allclose(Z, eval("base[%s]" % index)))
    
    # First column
    Z = base[:,0]
    index = find_index(base,Z)
    debug_print(index)
    print(np.allclose(Z, eval("base[%s]" % index)))
    
    # First row
    Z = base[0,:]
    index = find_index(base,Z)
    debug_print(index)
    print(np.allclose(Z, eval("base[%s]" % index)))
    
    # Partial reverse
    Z = base[4:1:-1,6:2:-1]
    index = find_index(base,Z)
    debug_print(index)
    print(np.allclose(Z, eval("base[%s]" % index)))
    
    # # Full reverse
    Z = base[::-1,::-1]
    index = find_index(base,Z)
    debug_print(index)
    print(np.allclose(Z, eval("base[%s]" % index)))

    # Random
    Z = base[1:5:3,3:1:-1]
    index = find_index(base,Z)
    debug_print(index)
    print(np.allclose(Z, eval("base[%s]" % index)))


if __name__ == '__main__':
    test_find_index()
