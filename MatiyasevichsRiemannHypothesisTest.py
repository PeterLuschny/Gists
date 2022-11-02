# Yu. V. Matiyasevich's Riemann Hypothesis test.
# The sequence as defined by the Python program
# is infinite if and only if the Riemann Hypotheses
# is true, in which case the program never halts;
# otherwise it returns a negative number.

from math import gcd


def RiemannTest(stop: int) -> int | None:
    d = m = p = 0
    f0 = f1 = f3 = n = q = r = 1
    b = True

    # The condition "n <= stop" is added only
    # to save the tester's resources.
    while r >= 0 and n <= stop:
        print(r, end=", ")
        d *= 2 * n
        d += -f1 if (b := not b) else f1
        n += 1
        g = gcd(n, q)
        q = (n * q) // g
        if g == 1:
            p += 1
        m = 0
        q2 = q
        while q2 > 1:
            q2 //= 2
            m += d
        f1 = 2 * f0
        f0 *= 2 * n
        f3 *= 2 * n + 3
        r = f3 - p * p * (m - f0)
    if n < stop:
        print("Bad luck, Bernhard!")
        return r


RiemannTest(22)
