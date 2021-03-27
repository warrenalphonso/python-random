from signal import signal, alarm, SIGALRM
from contextlib import contextmanager


@contextmanager
def timeout(seconds: int):
    """Timeout a block of code after `seconds`.
    From: https://martinheinz.dev/blog/34
    """
    def timeout_handler(signum, frame):
        raise TimeoutError(
            f"TIMEOUT: Code execution exceeded {seconds} seconds.")

    if seconds <= 0:
        raise ValueError("Seconds must be positive.")

    try:
        # Register SIGALARM handler
        signal(SIGALRM, timeout_handler)
        # Set SIGALARM to run after seconds
        alarm(seconds)

        yield
    finally:
        # Cancel schedule SIGALARM
        alarm(0)
