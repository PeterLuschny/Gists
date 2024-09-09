import time
from typing import Callable

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


def Benchmark(T: Callable[[int, int], int]) -> list[float]:
    B: list[float] = []
    for s in [16, 32, 64, 128, 256]:
        t = Timer(str(s))
        t.start()
        [[T(n, k) for k in range(n + 1)] for n in range(s)]
        B.append(t.stop())
    return [B[1]/B[0], B[2]/B[1], B[3]/B[2], B[4]/B[3]]


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

from functools import cache, lru_cache

# polyatree ------------------------------------------
# https://codegolf.stackexchange.com/questions/275413/


@cache
def polya_tree(n: int, k: int) -> int:
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
    if k >  n: return polya_tree(n, n)
    if k <= 0: return 0
    if n == 1: return 0 if k == 0 else 1

    def W(n: int, k: int, u: int, w: int) -> int: 
       q, r = divmod(u, w)
       if r != 0: return 0
       return q * polya_tree(k, n) * polya_tree(q, n - 1)

    return sum(sum(W(k, i, n - i, j) 
           for i in range(1, n)) for j in range(1, n)) // (n - 1)


# tree_count ------------------------------------------------
# Jonathan Allan, https://codegolf.stackexchange.com/a/275420


@lru_cache(maxsize=None)
def tree_count(nodes: int, max_height: int) -> int:
    if nodes == 1:
        return int(max_height > 0)
    return sum(sum(tree_count(i, max_height) * (m := (nodes - i) // d)
                    * tree_count(m, max_height - 1)
                    for d in range(1, nodes - i + 1)
                    if (nodes - i) % d == 0
                  ) for i in range(1, nodes)
              ) // (nodes - 1)


# Results  ------------------------------------

if __name__ == "__main__":

    print("polya_tree", Benchmark(polya_tree))
    print("tree_count", Benchmark(tree_count))

    """
               16 0.0085 sec
               32 0.1437 sec
               64 1.5740 sec
              128 24.4983 sec
              256 392.6860 sec

    polya_tree [16.8, 10.9, 15.6, 16.1]

               16 0.0072 sec
               32 0.0844 sec
               64 0.8911 sec
              128 10.8109 sec
              256 140.7037 sec

    tree_count [11.7, 10.6, 12.1, 13.0]
    """