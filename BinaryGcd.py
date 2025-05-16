count = 0

def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor (GCD) using the binary GCD algorithm."""

    global count
    # count = 0 

    # Handle negative inputs for correctness.
    if a < 0: a = -a
    if b < 0: b = -b

    # Handle the corner cases.
    if a == 0: return b
    if b == 0: return a
    if a == b: return b

    # Count Trailing Zeros (CTZ) of x.
    # (x & -x) isolates the lowest set bit. 
    # .bit_length() gives the number of bits 
    # needed to represent that isolated bit.
    # -1 subtracting 1 converts this to the 
    # count of trailing zeros.

    # az = CTZ of a.
    az = (a & -a).bit_length() - 1
    # bz = CTZ of b.
    bz = (b & -b).bit_length() - 1
    
    # shift = common factors of 2 shared by a and b.
    shift = min(az, bz)

    # Remove all original trailing zeros from a to make it odd.
    # a is now the odd part of the original a.
    a >>= az 

    # Remove all original trailing zeros from b to make it odd.
    # b is now the odd part of the original b.
    b >>= bz 
    
    # Loop invariant: 'a' and 'b' are always odd here.
    # The loop ends when 'a' and 'b' are equal.
    while b != a:

        # print(a, b)
        count += 1

        d = abs(a - b) # Difference 'd' will be even (odd - odd = even).

        # Calculate CTZ of d for the next iteration's 'a'.
        # (d & -d) isolates LSB of abs(d) correctly for 2's complement.
        dz = (d & -d).bit_length() - 1 

        # The new 'b' for the next iteration is min of the current odd 'a' and odd 'b'.
        b = min(a, b) 

        # The new 'a' for the next iteration is abs(d) with removed trailing zeros from d to make it odd.
        a = d >> dz

    # print(f"Number of iterations was {count}.")

    # Restore common factors of 2 that were removed.
    return a << shift


if __name__ == "__main__":
    import math
    
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

    """ To trace the computation remove the hashtag 
    at the start of the while-loop. """

    print("\nThe gcd of 40902 and 24140 is", gcd(40902, 24140))

    """ 
    Output:

    40902 24140
    20451 6035
    901 6035
    2567 901
    833 901
    17 833
    51 17
    34
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

    print("\nA383441(n) is the number of iterations needed in the binary GCD algorithm to compute gcd(n, k) for k from 0 to n (using the above implementation). The corresponding gcd's are in A109004. The sequence starts at n = 0 and the first 62 terms of A383441 are:\n")

    def A383441(n: int) -> int:
        global count
        count = 0
        for k in range(n + 1): gcd(n, k)
        return count

    # print([n*math.log(n)/A383441(n) for n in range(1000,2000)])