
# The algorithm binary GCD of two nonnegative numbers 
# * is described in TAOCP, volume 2, section 4.5.2, page 321 of the 2nd edition,
# * is also known as Stein's algorithm,
# * is based on the fact that the GCD of two numbers is the same as the GCD of 
#   their difference and the smaller number.

# Knuth describes the advantages of the algorithm:
# "The algorithm requires no division instruction; it relies solely on the operations of
# (i) subtraction, (ii) testing whether a number is even or odd, and (iii) shifting
# the binary representation of an even number to the right."

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
    
    # Reduce to save same unnecessary iterations.
    if a > b and b > (a >> 1): 
        b = a - b
    elif b > a and a > (b >> 1): 
        a = b - a

    # CTZ - Count Trailing Zeros of x.
    # Counting trailing zeros is relevant because the binary GCD algorithm
    # removes all factors of 2 from the numbers by shifting their binary 
    # representation to the right. 
    # (x & -x) isolates the lowest set bit.
    # .bit_length() gives the number of bits needed to represent that isolated bit.
    # -1 Subtracting 1 converts this to the count of trailing zeros.

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

        if trac: print(a, b)
        count += 1

        # Difference 'd' will be odd (odd - odd = even).
        d = a - b if a > b else b - a

        # Calculate CTZ of d for the next iteration's 'a'.
        # (d & -d) isolates LSB of abs(a - b).
        dz = (d & -d).bit_length() - 1

        # The new 'b' for the next iteration is min of 
        # the current odd 'a' and odd 'b'.
        b = a if a < b else b

        # The new 'a' for the next iteration is d with 
        # removed trailing zeros to make it odd.
        a = d >> dz

    # print(f"Number of iterations was {count}.")

    # Restore common factors of 2 that were removed.
    return a << shift


# === Test ==========================================

if __name__ == "__main__":

    import math
    from timeit import default_timer as timer
    
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
    binary GCD algorithm to compute gcd(n, k) for k from 0 to n (using 
    the above implementation). The corresponding gcd's are in A109004. 
    [Edit: Meanwhile we optimized the implementation a bit so that the number
    of iterations here is even less than the counts given in A383441.]
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
    The following implementation is from Rosetta Code:
    https://rosettacode.org/wiki/Greatest_common_divisor#Iterative_binary_algorithm_8

    It claims to implement Algorithm B given by Don Knuth in TAOCP, 
    volume 2, section 4.5.2, page 321 of the second edition.
    """

    def gcd_bin(u: int, v: int, trac: bool = False) -> int:
        global count

        u, v = abs(u), abs(v)  # u >= 0, v >= 0
        if u < v:
            u, v = v, u  # u >= v >= 0
        if v == 0:
            return u

        # u >= v > 0
        k = 1
        while u & 1 == 0 and v & 1 == 0:  # u, v - even
            u >>= 1
            v >>= 1
            k <<= 1

        t = -v if u & 1 else u

        while t:
        
            if trac: print(u, v)
            count += 1

            while t & 1 == 0:
                t >>= 1
            if t > 0:
                u = t
            else:
                v = -t
            t = u - v

        return u * k

    """
    So let's compare the number of iterations needed using the two implementations."""

    def B383441(n: int) -> int:
        global count
        count = 0
        for k in range(n + 1):
            gcd_bin(n, k)
        return count

    print([B383441(n) for n in range(62)])
    
    """
    [0, 0, 0, 2, 0, 4, 4, 12, 2, 8, 10, 22, 10, 28, 24, 30, 10, 32, 22, 42, 24, 38, 46, 68, 26, 58, 58, 68, 54, 94, 62, 102, 34, 68, 76, 74, 52, 116, 94, 112, 62, 120, 84, 146, 102, 122, 140, 166, 70, 154, 126, 154, 128, 188, 144, 182, 124, 178, 192, 222, 138, 244]
    
    [0, 1, 2, 5, 5, 10, 11, 19, 13, 20, 22, 34, 25, 42, 41, 46, 33, 55, 44, 66, 51, 63, 73, 93, 59, 88, 90, 99, 90, 125, 99, 135, 81, 113, 118, 121, 100, 160, 141, 157, 117, 171, 136, 195, 159, 173, 197, 221, 138, 212, 188, 215, 196, 250, 211, 243, 200, 244, 264, 288, 217, 312]
    """
    
    def AK383441(n: int) -> list[int]:
        global count
        L = []
        for k in range(n + 1):
            count = 0
            gcd(n, k)
            L.append(count)
        return L

    for n in range(13): print(AK383441(n))
    
    def BK383441(n: int) -> list[int]:
        global count
        L = []
        for k in range(n + 1):
            count = 0
            gcd_bin(n, k)
            L.append(count)
        return L

    for n in range(13): print(BK383441(n))

    # for n in range(50): print([n], A383441(n), B383441(n))

    """ To trace the computation call the function with 
    a third parameter 'True'. """
    
    print("\nThe gcd of 40902 and 24140 is:")
    gcd(40902, 24140, True)
    print("\nThe gcd of 40902 and 24140 is:")
    gcd_bin(40902, 24140, True)
    print()

    s = """\nThe number of iterations in our implementation is always smaller than in the Rosetta Code implementation of Knuth's presentation. Maybe this is a bug in the Rosetta Code implementation or just another variant.\n"""
    print(s)

    start = timer()
    [A383441(n) for n in range(1000)]
    end = timer()
    L = 1000
    print(f"Elapsed time for {L} rows is {end - start} seconds.\n")

    """ Time for n =  1000 :   1.53 seconds."""
    """ Time for n = 10000 : 284.94 seconds."""
