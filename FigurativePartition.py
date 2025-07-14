'''
                          FIGURATIVE PARTITIONS

We study decreasing index paths in two-dimensional arrays that sum up to a given 
total t if evaluated by a generating function A. The arrays are denoted by A(n, k) 
for n >= 0 and k >= 0. A path is a list of index pairs W = [i_0, i_1, ..., i_m] 
where the index pairs i_j = (n_j, k_j) are subject to the condition 

       'n_j > n_{j+1} and k_j >  k_{j+1}' (case A385900), 
    or 'n_j > n_{j+1} and k_j >= k_{j+1}' (case A385901).

The values of the generating function A sum to a prescribed positive number 
t = Sum_{(n, k) in W} A(n, k). We call n the 'color' and k the 'shade' of A(n, k).

Here we consider the array A139600 with the generating function

    P(n, k) = k + n * (k - 1) * k / 2 for n >= 0, k >= 2,

supplemented by the condition P(n, 1) = 1 if n = 0 otherwise 0.

The array starts with the first row being the nonnegative integers, then 
triangular numbers, squares, pentagonal, etc., the columns begin at k = 2, 
and the case k = 1 is treated as an exceptional case.

    Nonnegatives . A001477: 0,  1,  2,  3,  4,   5,   6,   7, ...
    Triangulars .. A000217: 0,  1,  3,  6, 10,  15,  21,  28, ...
    Squares ...... A000290: 0,  1,  4,  9, 16,  25,  36,  49, ...
    Pentagonals .. A000326: 0,  1,  5, 12, 22,  35,  51,  70, ...
    Hexagonals ... A000384: 0,  1,  6, 15, 28,  45,  66,  91, ...
    Heptagonals .. A000566: 0,  1,  7, 18, 34,  55,  81, 112, ...
    Octagonals ... A000567: 0,  1,  8, 21, 40,  65,  96, 133, ...
    9-gonals ..... A001106: 0,  1,  9, 24, 46,  75, 111, 154, ...
    10-gonals .... A001107: 0,  1, 10, 27, 52,  85, 126, 175, ...
    11-gonals .... A051682: 0,  1, 11, 30, 58,  95, 141, 196, ...
    12-gonals .... A051624: 0,  1, 12, 33, 64, 105, 156, 217, ...

We call F = [(i, j) in W: P(i, j)] a 'figurative partition of n' if Sum(F) = n. 
In the context of figurative partitions, we call n the 'shape' and k the 'size' 
of P(n, k). (See also the plots of Stefan Friedrich Birkner at 
https://oeis.org/wiki/User:Peter_Luschny/FigurateNumber.)

For example, in the case A385900 (strictly descending) the path 
W = [(3, 4), (2, 2), (0, 1)] leads to F = 22 + 4 + 1, which is a figurative 
partition of 27. In other words, 27 has a figurative layout on a counting board 
with a pentagon of size 4, a square of size 2, and a 'pebble', the unique 
figurative partition of 1. Another figurative partition of 27 is an octagon of 
size 3, a pentagon of size 2, plus a pebble.

In the weakly descending case A385901, some examples for figurative partitions 
of 27 are, in the format '(shape, size) value':

    (6, 3) 21 + (2, 2) 4 + (0, 2) 2;
    (5, 3) 18 + (3, 2) 5 + (1, 2) 3 + (0, 1) 1;
    (5, 3) 18 + (1, 3) 6 + (0, 3) 3;
    (4, 3) 15 + (3, 2) 5 + (2, 2) 4 + (1, 2) 3.

The question: given a positive integer n, how many figurative partitions of n exist?

    https://oeis.org/A385900 (strictly decreasing index paths)
    https://oeis.org/A385901 (weakly decreasing index paths)
    https://oeis.org/A139600 (partition function P(n, k))
'''

def P(n: int, k: int) -> int:
    """
    Return the value of the figurative partition function P(n, k) as defined 
    above, for n >= 1 and k >= 1.
    """
    if k == 1: return 1 if n == 0 else 0
    return k + n * (k - 1) * k // 2


def gen_fig_parts(m: int) -> list[list[tuple[int, int]]]:
    """
    Return all figurative partitions W(m) as lists of (n, k) tuples,
    where P(n, k) = k + n * (k-1) * k // 2 and both n, k decrease along the path.
    Choose between strictly decreasing (A385900) and weakly decreasing (A385901) 
    by modifying the condition in the DFS (Depth-First Search).
    """
    
    # Precompute all (n, k, value) with value <= m
    vals = []
    for k in range(1, m + 1):
        n = 0
        while n < m:
            v = P(n, k)
            if v > m: break
            vals.append((n, k, v))
            n += 1

    # Sort them so that we always pick larger (n, k) first.
    vals.sort(key=lambda x: (x[0], x[1]), reverse=True)

    results = []
    # DFS: append each (n, k) if it stays within both decreasing-index
    # rules and doesn’t overshoot the remaining sum.
    def dfs(remaining, last_n, last_k, start_index, path) -> None:
        for i in range(start_index, len(vals)):
            n, k, v = vals[i]
            # prune by value
            if v > remaining:
                continue

            # enforce strictly decreasing index k
            # -- A385900
            #if n < last_n and k < last_k and v > 0:

            # enforce weakly decreasing index k
            # -- A385901 
            if n < last_n and k <= last_k and v > 0: 

                path.append((n, k))
                if v == remaining:
                    # found a full partition
                    results.append(path.copy())
                else:
                    dfs(remaining - v, n, k, i + 1, path)
                path.pop()

    # start with m + 1 for last_n, last_k so any (n, k) is allowed first.
    dfs(m, m + 1, m + 1, 0, [])
    return results


def num_fig_parts(n: int) -> int:
    return len(gen_fig_parts(n))


def show_fig_parts(n: int) -> None:
    print(f"** The figurative partitions of {n} are:")
    fp = gen_fig_parts(n)
    for all_parts in fp:
        a = ''
        for p in all_parts:
            q = P(p[0], p[1])
            print(a, p, q, end=' ')
            a = '+'
        print()
    print("The paths of the partitions are:")
    print(fp)
    print(len(fp), "figurative partitions of", n, "found.\n")


# Examples:
if __name__ == "__main__":

    for n in range(1, 7):
        show_fig_parts(n)
    print()

    print([len(gen_fig_parts(n)) for n in range(1, 17)])


"""
I asked ChatGPT to give a  **Summary**  of the above, and it answered:

This work studies *figurative partitions* of a positive integer `n` using paths 
through a 2D array `A(n, k)` defined by a generating function `P(n, k)`. 
A figurative partition of `n` is a sequence of index pairs `(n, k)` such that the 
sum of `P` values along a path equals `n`. Paths must follow either strictly 
decreasing (`A385900`) or weakly decreasing (`A385901`) index rules. The function
`P(n, k)` generates figurate numbers (e.g., triangular, square, pentagonal) based 
on `n` (the shape of the figure) and `k` (the size of the figure). The code generates
all valid figurative partitions of `n` via depth-first search over eligible `(n, k)`
pairs, and returns their count or full list. This results in a combinatorial inter-
pretation of `n` as a sum of figurate numbers under specific structural constraints.
"""
