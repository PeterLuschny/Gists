def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor (GCD) using the binary GCD algorithm."""

    # Handle negative inputs for correctness
    if a < 0: a = -a
    if b < 0: b = -b

    if a == 0: return b
    if b == 0: return a

    # az = Count Trailing Zeros (CTZ) of a.
    # (x & -x) isolates the lowest set bit. 
    # .bit_length() - 1 gives its exponent.
    az = (a & -a).bit_length() - 1
    # bz = CTZ of b.
    bz = (b & -b).bit_length() - 1
    
    # shift = common factors of 2 shared by a and b.
    shift = min(az, bz)
    
    # Remove all original trailing zeros from b to make it odd.
    # b is now the odd part of the original b.
    b >>= bz 
    
    # Loop invariant: 'b' is always odd here.
    # 'a' will be made odd at the start of the loop using its CTZ ('az').
    # 'az' initially is CTZ of original 'a'. In subsequent loops, it's CTZ of abs(d).
    while True:
        # Make 'a' odd by removing its trailing zeros.
        # (a >> az) is the odd part of the current 'a'.
        a >>= az 
        
        # Now 'a' and 'b' are both odd.
        d = b - a # Difference 'd' will be even (odd - odd = even).
        
        if d == 0:
            # If d is 0, then 'a' (the odd part) and 'b' (the odd part) were equal.
            # This 'a' (or 'b') is the odd part of the GCD.
            # Restore common factors of 2.
            return a << shift
        
        # Calculate CTZ of d for the next iteration's 'a'.
        # (d can be negative, but (d & -d) isolates LSB of abs(d) correctly for 2's complement)
        az = (d & -d).bit_length() - 1 
        
        # The new 'b' for the next iteration is min of the current odd 'a' and odd 'b'.
        b = min(a, b) # a is a_odd here, b is b_odd from start of this iteration.

        # The new 'a' for the next iteration is abs(d).
        # This 'a' is even (or 0 if d was 0, but that's handled).
        # It will be shifted by the new 'az' at the start of the next loop.
        a = abs(d)


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