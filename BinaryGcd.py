# The algorithm binary GCD of two nonnegative numbers
# * is described in TAOCP, volume 2, section 4.5.2, page 321 of the 2nd edition,
# * is also known as Stein's algorithm,
# * is based on the fact that the GCD of two numbers is the same as the GCD of
#   their difference and the smaller number.

# Knuth describes the advantages of the algorithm:
# "The algorithm requires no division instruction; it relies solely on the operations of
# (i) subtraction, (ii) testing whether a number is even or odd, and (iii) shifting
# the binary representation of an even number to the right."

# Our goal is to compare this algorithm, as described by Knuth, 
# with a variant that can be found in various places on the Internet. 
# For example, it is described by Sergey Slotin et al. on Algorithmica.org. 
# https://en.algorithmica.org/hpc/algorithms/gcd/ where it says: 
# "The main optimization ideas belong to Daniel Lemire and Ralph Corderoy, 
# who had nothing better to do on the Christmas holidays of 2013."
# (We have no way to verify this.)

# The global variable 'count' records the number of iteration executed in GCD.
count = 0


def gcd(a: int, b: int, trac: bool = False) -> int:
    """Compute the greatest common divisor (GCD) using the binary GCD algorithm."""

    global count

    # Handle negative inputs for correctness.
    if a < 0:
        a = -a
    if b < 0:
        b = -b

    # Handle the corner cases.
    if a == 0:
        return b
    if b == 0:
        return a
    if a == b:
        return b

    if trac:
        print(a, b)

    # Gives gcd(a, b) and gcd(a, a - b) the same number of iterations
    # if a > b and saves some iterations.
    if a > b and b > (a >> 1):
        b = a - b
    elif b > a and a > (b >> 1):
        a = b - a

    # If you look at the triangle gcd(n, k) for 0 <= k <= n, (OEIS A109004)
    # you will see that the rows are symmetric in the sense that
    # gcd(n, k) = gcd(n, n - k). 
    # It's very counterintuitive when analyzing Stein's algorithm as described 
    # by Knuth that the number of iterations for the right-hand value is larger, 
    # often many times larger, than the number of iterations required for the 
    # left-hand value. One can also understand this as an optimization. 
    # We address this with the above assignment. See also the table of counts
    # in the test section below.

    # CTZ - Count Trailing Zeros of x.
    # Counting trailing zeros is relevant because the binary GCD algorithm
    # removes all factors of 2 from the numbers by shifting their binary
    # representation to the right.
    # (x & -x) isolates the lowest set bit.
    # .bit_length() gives the number of bits needed to represent that isolated bit.
    # -1 Subtracting 1 converts this to the count of trailing zeros.
    
    # This quantity is used below in the form 
    # a = a >> ((a & -a).bit_length() - 1). 
    # It's not immediately obvious what this bit-fiddling means.
    # In the more civilized language of a CAS, for example with Maple, 
    # one would write a := odd(a), where odd := n -> n * 2^(-ordp(n, 2)),
    # and ordp(n, 2) is the 2-adic order of n. To put it in plain English, 
    # it is the odd part of n (OEIS A000265).

    # az = CTZ of a.
    az = (a & -a).bit_length() - 1
    # bz = CTZ of b.
    bz = (b & -b).bit_length() - 1

    # shift = common factors of 2 shared by a and b.
    shift = az if az < bz else bz

    # Remove all original trailing zeros from a to make it odd.
    # a is now the odd part of the original a.
    a >>= az

    # Same with b. b is now the odd part of the original b.
    b >>= bz

    # Loop invariant: 'a' and 'b' are always odd.
    # The loop ends when 'a' and 'b' are equal.
    while b != a:

        # For tracing and debugging only. Remove in production.
        if trac: print(a, b)
        count += 1

        # Differences will be odd (odd - odd = even).
        # The new 'b' for the next iteration is min of
        # the current odd 'a' and odd 'b'.
        if a < b:
            b, a = a, b - a 
        else:
            a = a - b

        # Calculate the CTZ of 'a' for the next iteration's 'a'.
        # (a & -a) isolates LSB of abs(a - b).
        # The new 'a' for the next iteration is a with
        # removed trailing zeros to make it odd.
        a = a >> ((a & -a).bit_length() - 1)

    # Restore common factors of 2 that were removed.
    return a << shift

"""
    Algorithm B as given by Don Knuth in TAOCP, volume 2, section 4.5.2, 
    page 321 of the second edition.
"""

def gcd_taocp(u: int, v: int, trac: bool = False) -> int:
    global count

    # Handle negative inputs for correctness.
    if u < 0:
        u = -u
    if v < 0:
        v = -v

    # Handle the corner cases.
    if u == 0:
        return v
    if v == 0:
        return u
    if u == v:
        return v

    if trac:
        print(u, v)

    # B1 Find power of 2.
    k = 0
    while u & 1 == 0 and v & 1 == 0:
        k += 1
        u >>= 1
        v >>= 1

    # B2 Initialize
    if u & 1:  # u - odd
        t = -v
    else:
        t = u

    # Main loop
    while t != 0:
        count += 1
        if trac:
            print(u, v)

        # B3 Is t odd?
        while t & 1 == 0:
            t >>= 1

        if t > 0:
            u = t
        else:
            v = -t

        # B4 Subtract
        t = u - v

    return u << k


# === Test ==========================================

if __name__ == "__main__":

    import math
    from timeit import default_timer as timer

    print("\nThe gcd(n, k) for 0 <= k <= n. In the OEIS A109004.\n")

    for n in range(13):
        print([gcd(n, k) for k in range(n + 1)])

    """
    Output:

        [ 0]
        [ 1, 1]
        [ 2, 1, 2]
        [ 3, 1, 1, 3]
        [ 4, 1, 2, 1, 4]
        [ 5, 1, 1, 1, 1, 5]
        [ 6, 1, 2, 3, 2, 1, 6]
        [ 7, 1, 1, 1, 1, 1, 1, 7]
        [ 8, 1, 2, 1, 4, 1, 2, 1, 8]
        [ 9, 1, 1, 3, 1, 1, 3, 1, 1, 9]
        [10, 1, 2, 1, 2, 5, 2, 1, 2, 1, 10]
        [11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11]
        [12, 1, 2, 3, 4, 1, 6, 1, 4, 3, 2, 1, 12]
    """

    print("\nTest the binary GCD against Python's built-in math.gcd function.")
    OK = True
    for n in range(100):
        for k in range(100):
            if gcd(n, k) != math.gcd(n, k):
                print(f"Error for {n} and {k}")
                OK = False
    if OK:
        print("All tests passed.")

    s = """\nA383441(n) is the number of iterations needed in the
    binary GCD algorithm to compute gcd(n, k) for 0 <= k <= n, 
    using our implementation. The corresponding gcd's are in A109004. 
    [Meanwhile we optimized the implementation a bit so that the number
    of iterations here is slightly less than the counts given in A383441.] 
    The sequence starts at n = 0 and the first 62 terms of A383441 are:\n"""
    print(s)

    def A383441(n: int) -> int:
        global count
        count = 0
        for k in range(n + 1):
            gcd(n, k)
        return count

    print([A383441(n) for n in range(62)])

    """
    Let's compare the number of iterations of the two implementations.
    """

    print("\nThe number of iterations in Knuth's TAOCP implementation is:")

    def B383441(n: int) -> int:
        global count
        count = 0
        for k in range(n + 1):
            gcd_taocp(n, k)
        return count

    print([B383441(n) for n in range(62)])
    print()

    """
    [0, 0, 0, 2, 0, 4, 4, 12, 2, 8, 10, 22, 10, 28, 24, 30, 10, 32, 22, 42, 24, 38, 46, 68]
    
    [0, 0, 1, 4, 4, 9, 10, 18, 12, 19, 21, 33, 24, 41, 40, 45, 32, 54, 43, 65, 50, 62, 72]
    """

    print(
        "\nComparing the number of iterations in the two implementations side by side."
    )
    print("| n | #A383441(n) | #TAOCP(n) | #TAOCP(n) - #A383441(n) |")
    for n in range(33):
        print(f"{n} | {A383441(n)} | {B383441(n)} | {B383441(n) - A383441(n)} |")

    print(
        "\nThe number of iterations in our implementation is always smaller."
    )

    """ To trace the computations call the functions with 
    a third parameter set to 'True'. """

    print("\nTracing the gcd of 40902 and 24140 with our version:")
    gcd(40902, 24140, True)
    print("Tracing the gcd of 40902 and 24140 with Knuth's TAOCP:")
    gcd_taocp(40902, 24140, True)
    print()
    
    from math import factorial
    f = factorial(1000)
    g = 2**32 + 1
    print("Tracing the gcd of factorial(1000) and 2**32 + 1 with our version:")
    count = 0
    print(f"gcd = {gcd(f, g)}, iterations: {count}")
    print("Tracing the gcd of factorial(1000) and 2**32 + 1 with Knuth's TAOCP:")
    count = 0
    print(f"gcd = {gcd_taocp(f, g)}, iterations: {count}")
    print()


    def AK383441(n: int) -> list[int]:
        global count
        L = []
        for k in range(n + 1):
            count = 0
            gcd(n, k)
            L.append(count)
        return L

    print(
        "The number of iterations in our implementation is symmetric in the sense\n gcd(max(a, b), min(a, b)) = gcd(max(a, b), max(a, b) - min(a, b)).\n"
    )

    for n in range(17):
        print([n], AK383441(n))

    def BK383441(n: int) -> list[int]:
        global count
        L = []
        for k in range(n + 1):
            count = 0
            gcd_taocp(n, k)
            L.append(count)
        return L

    print(
        "\nThe number of iterations in the TAOCP setup is not symmetric in the above sense.\n"
    )

    for n in range(17):
        print([n], BK383441(n))

    print("\nTiming the two implementations.\n")

    for L in [500, 1000]:
        start = timer()
        [A383441(n) for n in range(L)]
        end = timer()
        print(
            f"Elapsed time for {L} rows is {(end - start):2.2f} seconds [our version]."
        )

        start = timer()
        [B383441(n) for n in range(L)]
        end = timer()
        print(f"Elapsed time for {L} rows is {(end - start):2.2f} seconds [TAOCP].\n")

    """ Timing the two implementations.
    Elapsed time for 500 rows is 0.34 seconds [our version].
    Elapsed time for 500 rows is 0.48 seconds [TAOCP].

    Elapsed time for 1000 rows is 1.55 seconds [our version].
    Elapsed time for 1000 rows is 2.20 seconds [TAOCP].

    Elapsed time for 2000 rows is 6.93 seconds [our version].
    Elapsed time for 2000 rows is 9.62 seconds [TAOCP].
    """

    print()
