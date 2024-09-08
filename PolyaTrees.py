import time

class Timer:
    def __init__(
        self,
        comment: str
    ) -> None:
        self.start_time = None
        self.text = comment

    def start(self) -> None:
        """Start a new timer"""
        if self.start_time is not None:
            raise RuntimeError("Timer is running. First stop it.")
        self.start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self.start_time is None:
            raise RuntimeError("Timer is not running.")

        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

        print(self.text.rjust(17), "{:0.4f}".format(elapsed_time), "sec")

        return elapsed_time


""" Polya Trees
    [0] [0]
    [1] [0, 1]
    [2] [0, 0, 1]
    [3] [0, 0, 1,  2]
    [4] [0, 0, 1,  3,  4]
    [5] [0, 0, 1,  5,  8,   9]
    [6] [0, 0, 1,  7, 15,  19,  20]
    [7] [0, 0, 1, 11, 29,  42,  47,  48]
    [8] [0, 0, 1, 15, 53,  89, 108, 114, 115]
    [9] [0, 0, 1, 22, 98, 191, 252, 278, 285, 286]
"""

from functools import cache

@cache
def polyatree(n: int, k: int) -> int:
    """
    Args:
        n, the number of vertices
        k, level of a vertex, the level of a vertex is 
        the number of vertices in the path from the root 
        to the vertex, the level of the root is 1.

    Returns:
        number of rooted trees with n vertices where the
        level of a vertex is bounded by k.
    """
    if k >  n: return polyatree(n, n)
    if k <= 0: return 0
    if n == 1: return 0 if k == 0 else 1

    def W(n: int, k: int, u: int, w: int) -> int: 
       q, r = divmod(u, w)
       if r != 0: return 0
       return q * polyatree(k, n) * polyatree(q, n - 1)

    return sum(sum(W(k, i, n - i, j) 
           for i in range(1, n)) for j in range(1, n)) // (n - 1)


def Benchmark() -> list[float]:
    T: list[float] = []
    for s in [16, 32, 64, 128]:
        t = Timer(str(s))
        t.start()
        [[polyatree(n, k) for k in range(n + 1)] for n in range(s)]
        T.append(t.stop())
    return [T[1]/T[0], T[2]/T[1], T[3]/T[2]]


print(Benchmark())
