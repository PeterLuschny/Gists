# Using Python 3.12.4

import time
from typing import Callable, Generator

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
    for s in [16, 32, 64, 128, 256, 512]:
        t = Timer(str(s))
        t.start()
        [[T(n, k) for k in range(n + 1)] for n in range(s)]
        B.append(t.stop())
    return [B[i + 1] / B[i] for i in range(5)]


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


# tree_count ----------------------------------------------------------
# Jonathan Allan, https://codegolf.stackexchange.com/a/275420

@cache
def divisors(n: int) -> Generator[int, None, None]:
    return (d for d in range(n, 0, -1) if n % d == 0)

@cache
def tree_count(nodes: int, max_height: int) -> int:
    if nodes == 1:
        return int(max_height > 0)

    next_height = max_height - 1
    return sum(
        sum(
            tree_count(i, max_height) * d * tree_count(d, next_height)
            for d in divisors(nodes - i)
        )
        for i in range(1, nodes)
    ) // (nodes - 1)


# TreeCount -----------------------------------------------------------
# gsitcia

@cache
def Divisors(n: int) -> Generator[int, None, None]:
    return (d for d in range(n, 0, -1) if n % d == 0)

@cache
def TreeCount(nodes: int, max_height: int) -> int:
    if nodes == 1:
        return int(max_height > 0)
    if max_height == 0:
        return 0

    next_height = max_height - 1
    return sum(
        TreeCount(i, max_height) * TreeCount_1(nodes - i, next_height)
        for i in range(1, nodes)
    ) // (nodes - 1)


@cache
def TreeCount_1(nodes_i: int, next_height: int) -> int:
    return sum(d * TreeCount(d, next_height) for d in Divisors(nodes_i))


# Results  ----------------------------------------

if __name__ == "__main__":

    # print("polya_tree", Benchmark(polya_tree))
    print("tree_count", Benchmark(tree_count))
    print("TreeCount ", Benchmark(TreeCount))

    """
               16 0.0085 sec
               32 0.1437 sec
               64 1.5740 sec
              128 24.4983 sec
              256 392.6860 sec

    polya_tree [16.8, 10.9, 15.6, 16.1]

               16 0.0014 sec
               32 0.0080 sec
               64 0.0659 sec
              128 0.4913 sec
              256 3.7559 sec
              512 31.3221 sec

    tree_count [5.7, 8.2, 7.4, 7.6, 8.3]

               16 0.0016 sec
               32 0.0089 sec
               64 0.0672 sec
              128 0.5700 sec
              256 4.6278 sec
              512 44.6065 sec

    TreeCount  [5.6, 7.5, 8.5, 8.1, 9.6]
    """
