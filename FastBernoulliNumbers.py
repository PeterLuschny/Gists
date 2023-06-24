#################################################
#
# Here's the challenge: Compute the list of the
# first 1000 Bernoulli numbers. The definiton is:
# A164555/A027642 (followed by Tao and Knuth).
# 
# The fastest wins. To keep things comparable, 
# subject to the following conditions:
# 
# 1. Python (only using standard classes).
# 2. No more than 20 lines.
# 3. Max line length 40 characters.
#
#################################################
#
# My solution:

from functools import cache
from fractions import Fraction as frac 
@cache
def genocchi(n: int) -> list[int]:
    if n == 0: return [1]
    row = [0] + genocchi(n - 1) + [0]
    for k in range(n, 0, -1):
        row[k] += row[k + 1]
    for k in range(2, n + 2):
        row[k] += row[k - 1]
    return row[1:]
def Bernoulli(n: int) -> frac:
    if n < 2: 
        return frac(1, n + 1)
    if n % 2 == 1: 
        return frac(0, 1)
    g = genocchi(n // 2 - 1)[-1]
    f = frac(g, 2 ** (n + 1) - 2)
    return -f if n % 4 == 0 else f


if __name__ == "__main__":

    print([Bernoulli(n) for n in range(10)])

    from timeit import default_timer as timer
    start = timer()
    [Bernoulli(n) for n in range(1000)]
    end = timer()
    print(end - start) 

# Time on my computer: between 0.19 and 0.2 sec
