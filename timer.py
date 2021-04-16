from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timer():
    """Time a block of code within a `with` statement.
    with timer():
        # Do things

    From: https://martinheinz.dev/blog/34
    """
    try:
        start = perf_counter()
        yield
    finally:
        end = perf_counter()
        print(f"Time elapsed: {end - start} seconds")
