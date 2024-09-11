# Using Python 3.12.4

import time
from typing import Callable

class StopWatch:
    def __init__(
        self,
        comment: str = "elapsed time"
    ) -> None:
        self.start_time = None
        self.text = comment

    def start(self) -> None:
        """Start a new StopWatch"""
        if self.start_time is not None:
            raise RuntimeError("Watch is running. First stop it.")
        self.start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the StopWatch, and report the elapsed time."""
        if self.start_time is None:
            raise RuntimeError("Watch is not running.")

        elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

        print(self.text.rjust(17), "{:0.4f}".format(elapsed_time), "sec")

        return elapsed_time


def Benchmark(T: Callable[[int, int], int], 
              offset:int = 4, 
              size:int = 4
    ) -> list[float]:
    """Benchmark for functions computing lower triangular arrays.

    Args:
        T(n, k), function defined for n >= 0 and 0 <= k <= n.
        offset > 0, the power of two where the test starts. Defaults to 4.
        size, the length of test run. Defaults to 4.

    Returns:
        List of factors that indicate by what the computing time
        multiplies when the number of rows doubles.

    Example:
        Benchmark(lambda n, k: n**k)
    """
    B: list[float] = []
    for s in [2 << n for n in range(offset - 1, offset + size)]:
        t = StopWatch(str(s))
        t.start()
        [[T(n, k) for k in range(n + 1)] for n in range(s)]
        B.append(t.stop())
    return [B[i + 1] / B[i] for i in range(size)]


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
def divisors(n: int) -> list[int]:
    return [d for d in range(n, 0, -1) if n % d == 0]

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
# User gsitcia at the above link.
# We added the border cases T(n, n) and T(n-1, n), which was commented by 
# Jonathan Allan: "... the added overhead of the comparisons (performed 
# for all but 1 node or 0 max height) outweighs the savings of the small 
# number of pruned cases." 
# Answer: For nodes = 1024 it saved in our setup about 3 sec.

@cache
def Divisors(n: int) -> list[int]:
    return [d for d in range(n, 0, -1) if n % d == 0]

@cache
def TreeCount_1(nodes_i: int, next_height: int) -> int:
    return sum(d * TreeCount(d, next_height) for d in Divisors(nodes_i))

@cache
def TreeCount(nodes: int, max_height: int) -> int:
    if nodes == 1:
        return int(max_height > 0)
    if max_height == 0:
        return 0
    if nodes - 1 == max_height:
        return TreeCount(nodes, nodes - 2) + max_height - 1
    if nodes == max_height: 
        return TreeCount(nodes, nodes - 1) + 1

    next_height = max_height - 1
    return sum(
        TreeCount(i, max_height) * TreeCount_1(nodes - i, next_height)
        for i in range(1, nodes)
    ) // (nodes - 1)


# Results  ----------------------------------------

if __name__ == "__main__":

    for n in range(10):
        print([tree_count(n, k) for k in range(n + 1)])
        print([TreeCount(n, k)  for k in range(n + 1)])

    # print("polya_tree", Benchmark(polya_tree, 4, 4))
    print("tree_count", Benchmark(tree_count, 4, 4))
    print("TreeCount ", Benchmark(TreeCount,  4, 6))

    """
               16 0.0085 sec
               32 0.1437 sec
               64 1.5740 sec
              128 24.4983 sec
              256 392.6860 sec

    polya_tree [16.8, 10.9, 15.6, 16.1]

               16 0.0069 sec
               32 0.0662 sec
               64 0.6862 sec
              128 4.8875 sec
              256 47.5928 sec

    tree_count [9.6, 10.4, 7.1, 9.7]

               16 0.0012 sec
               32 0.0108 sec
               64 0.1052 sec
              128 0.7198 sec
              256 6.3722 sec

              512 71.4239 sec
             1024 915.5698 sec

    TreeCount  [8.9, 9.7, 6.8, 8.8, 11.2, 12.8]


    ===========================================================
    =================== M A P L E =============================
    ===========================================================

    restart;

    div := n -> numtheory:-divisors(n):
    H := proc(n, k) option remember; local d; 
         add(d * T(d, k), d = div(n)) end: 

    T := proc(n, k) option remember; local i; 
         if n = 1 then ifelse(k > 0, 1, 0) else
         add(T(i, k) * H(n - i, k - 1), i = 1..n - 1) / (n - 1)
         fi end:


    Tri := rows -> local n, k; 
           seq(seq(T(n, k), k = 0..n), n = 0..rows):

    gc(); CodeTools:-Usage(Tri(64)):
    gc(); CodeTools:-Usage(Tri(128)):
    gc(); CodeTools:-Usage(Tri(256)):
    gc(); CodeTools:-Usage(Tri(512)):

    memory used=18.29MiB,  real time=375.00ms, gc time=0ns
    memory used=151.96MiB, real time=2.86s,    gc time=140.62ms
    memory used=1.42GiB,   real time=24.16s,   gc time=1.56s
    memory used=15.16GiB,  real time=3.81m,    gc time=35.25s

    """
