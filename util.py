from itertools import tee, izip, imap, izip_longest
import numpy


def axis_dict_to_tuple(axes):
    return (axes['x'], axes['y'], axes['z'])

def rolling_window(iterable, window_size=2):
    """
    Create an iterable moving window of `window_size` over `iterable`
    """
    iterables = tee(iterable, window_size)

    # step each tee'ed iterator
    for i in xrange(1, window_size):
        for iterable in iterables[i:]:
            next(iterable, None)

    # create iterable from list of iterators
    return izip(*iterables)

def smooth_measurements(X, size=3):
    return imap(numpy.mean, rolling_window(X, size))

def smooth_3d_measurements(X, size=3):
    for x, y, z in imap(lambda e: zip(*e), rolling_window(X, 3)):
        yield (numpy.mean(axis) for axis in (x, y, z))
