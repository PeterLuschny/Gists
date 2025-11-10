#!/usr/bin/env python3
import math
from collections import defaultdict
from collections.abc import Iterator
from functools import lru_cache, cmp_to_key
from typing import NamedTuple
# from tqdm import tqdm

# ---------- Data structures ----------

class HalfEntry(NamedTuple):
    """Represents a partial Egyptian fraction sum."""
    num: int
    den: int
    mask: int        # bitmask of denominators used
    max_denom: int   # largest denominator in this subset

class Match(NamedTuple):
    """Represents a full unit-sum obstruction."""
    mask: int
    max_denom: int

# ---------- Utilities ----------

def add_one_over_n(pair: tuple[int, int], n: int) -> tuple[int, int]:
    num, den = pair
    nnum = num * n + den
    nden = den * n
    g = math.gcd(nnum, nden)
    return (nnum // g, nden // g)

def rational_cmp(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Exact comparison of rationals a=(num,den), b=(num,den).
    Return negative if a < b, zero if equal, positive if a > b.
    """
    an, ad = a
    bn, bd = b
    lhs = an * bd
    rhs = bn * ad
    return (lhs > rhs) - (lhs < rhs)

# ---------- Build half lists ----------

def build_half_list(lo: int, hi: int) -> list[HalfEntry]:
    """
    Build all subset sums of {1/k : k in [lo, hi)} that are <= 1.
    Returns a list of HalfEntry sorted by rational value.
    """
    entries: list[tuple[tuple[int, int], int, int]] = [((0, 1), 0, 0)]
    for n in range(lo, hi):
        add: list[tuple[tuple[int, int], int, int]] = []
        for (pair, mask, curmax) in entries:
            new_pair = add_one_over_n(pair, n)
            if new_pair[0] <= new_pair[1]:
                new_mask = mask | (1 << (n - 1))
                new_max = max(curmax, n)
                add.append((new_pair, new_mask, new_max))
        entries.extend(add)

    result = [HalfEntry(p[0], p[1], m, mx) for (p, m, mx) in entries]
    result.sort(key=cmp_to_key(
        lambda x, y: rational_cmp((x.num, x.den), (y.num, y.den))))
    return result

# ---------- Two-pointer join ----------

def stream_unit_matches(
    left_list: list[HalfEntry], 
    right_list: list[HalfEntry]
) -> Iterator[Match]:
    """
    Stream all matches where left + right == 1.
    Yields Match(mask, max_denom).
    """
    i = 0
    j = len(right_list) - 1
    while i < len(left_list) and j >= 0:
        ln, ld, lmask, lmax = left_list[i]
        rn, rd, rmask, rmax = right_list[j]
        lhs = ln * rd + rn * ld
        rhs = ld * rd
        if lhs == rhs:
            # collect duplicates
            left_eq: list[HalfEntry] = []
            val_i = i
            while val_i < len(left_list):
                a = left_list[val_i]
                if a.num * ld != ln * a.den:
                    break
                left_eq.append(a)
                val_i += 1
            right_eq: list[HalfEntry] = []
            val_j = j
            while val_j >= 0:
                b = right_list[val_j]
                if rn * b.den != b.num * rd:
                    break
                right_eq.append(b)
                val_j -= 1
            for a in left_eq:
                for b in right_eq:
                    yield Match(a.mask | b.mask, max(a.max_denom, b.max_denom))
            i = val_i
            j = val_j
        elif lhs < rhs:
            i += 1
        else:
            j -= 1

# ---------- Hitting-set solver ----------

def exists_hitting_set(
    elem_to_mask: dict[int, int], 
    num_obs: int, 
    permitted: int
) -> bool:
    """
    Decide whether there exists a hitting set of size <= permitted
    covering all obstructions.
    Obstructions are represented by bits in masks.
    """
    full_mask = (1 << num_obs) - 1

    @lru_cache(maxsize=None)
    def solve(remaining_mask: int, k: int) -> bool:
        if remaining_mask == 0:
            return True
        if k == 0:
            return False

        rem = remaining_mask.bit_count()
        
        # dynamic max coverage among elements w.r.t remaining_mask
        max_cov = 0
        candidates: list[tuple[int, int]] = []
        for mask in elem_to_mask.values():
            cov = mask & remaining_mask
            if cov:
                c = cov.bit_count()
                candidates.append((c, cov))
                max_cov = max(max_cov, c)

        if max_cov == 0:
            return False
        if math.ceil(rem / max_cov) > k:
            return False

        # branch on elements in descending coverage order
        candidates.sort(reverse=True)
        for _, covmask in candidates:
            if solve(remaining_mask & ~covmask, k - 1):
                return True
        return False

    return solve(full_mask, permitted)

# ---------- Main routine ----------

def A390393List(N: int) -> list[int]:
    """
    Returns [a(1), ..., a(N-1)] using streaming meet-in-the-middle.
    """
    if N <= 1:
        return []

    split = N * 5 // 9
    left_list = build_half_list(1, split)
    right_list = build_half_list(split, N)

    buckets: dict[int, list[int]] = defaultdict(list)
    for match in stream_unit_matches(left_list, right_list):
        buckets[match.max_denom].append(match.mask)

    results: list[int] = []
    current_obs_masks: list[int] = []
    current_k = 0

    for n in range(1, N):
    # for n in tqdm(range(1, N), desc="Computing A390393", unit="n"):

        if n in buckets:
            current_obs_masks.extend(buckets[n])

        if not current_obs_masks:
            results.append(n)
            current_k = 0
            continue

        m = len(current_obs_masks)
        elem_to_mask: dict[int, int] = {}
        for idx, obs_mask in enumerate(current_obs_masks):
            mask = obs_mask
            while mask:
                lowbit = mask & -mask
                dpos = lowbit.bit_length() - 1
                denom = dpos + 1
                if denom <= n:
                    elem_to_mask[denom] = elem_to_mask.get(denom, 0) | (1 << idx)
                mask &= mask - 1

        found_k = None
        for k in range(current_k, n + 1):
            if exists_hitting_set(elem_to_mask, m, k):
                found_k = k
                current_k = k
                results.append(n - k)
                break
        if found_k is None:
            results.append(0)
            current_k = n

    return results


# ---------- Example run ----------

if __name__ == "__main__":
    N = 62 + 1
    print(f"Computing A390393 a(1)..a({N-1}) (N={N})")
    a_list = A390393List(N)
    print(a_list)

    import math
    import statistics
    from collections.abc import Callable

    Predictor = Callable[[int], tuple[float, float, float]]
    parameters = {"s0": 0.0, "A": 0.0, "C": 0.0, "sigma": 0.0}
    title = "A390393 observed vs model: â(n) = s0*n - A*ln(n) - C"

    def fit_s0_log_model(a_list) -> Predictor:
        # a_list: list of a(1)..a(M)
        s0 = 1.0 - math.exp(-1.0)
        M = len(a_list)
        xs = [math.log(n) for n in range(1, M+1)]
        ys = [s0 * n - a for n, a in zip(range(1, M+1), a_list)]
        xbar = statistics.mean(xs)
        ybar = statistics.mean(ys)
        Sxx = sum((x - xbar)**2 for x in xs)
        Sxy = sum((x - xbar)*(y - ybar) for x, y in zip(xs, ys))
        A = Sxy / Sxx if Sxx != 0 else 0.0
        C = ybar - A * xbar
        # residuals and std err
        residuals = [y - (A*x + C) for x, y in zip(xs, ys)]
        df = max(1, M - 2)
        sigma = math.sqrt(sum(r*r for r in residuals) / df)
        parameters["s0"] = s0
        parameters["A"] = A
        parameters["C"] = C
        parameters["sigma"] = sigma 

        def fit(n: int) -> tuple[float, float, float]:
            # Return (a_hat, lower95, upper95) for integer n >= 1.
            if n < 1: raise ValueError("n must be >= 1")
            k_hat = A * math.log(n) + C   # predicted residual s0*n - a(n)
            a_hat = s0 * n - k_hat
            lo = a_hat - 1.96 * sigma
            hi = a_hat + 1.96 * sigma
            return a_hat, lo, hi

        return fit

    fit = fit_s0_log_model(a_list)

    print("Fitted parameters:")
    print(f"  s0 = {parameters['s0']:.12f}")
    print(f"  A  = {parameters['A']:.6f}")
    print(f"  C  = {parameters['C']:.6f}")
    print(f"  sigma (resid std) = {parameters['sigma']:.6f}")

    print(title)
    for n in [10, 20, 30, 40, 50, 60, 70, 80]:
        a_hat, lo, hi = fit(n)
        v = a_list[n-1] if n <= len(a_list) else "--"
        print(f"n = {n}: a({n}) = {v}, predicted {round(a_hat)} (95% CI: [{lo:.2f}, {hi:.2f}])")


    import matplotlib.pyplot as plt

    # Plot observed a_list for n=1..M and estimated â(n) from the fit callable.
    # If n_extrapolate > 0, plot estimates up to n = M + n_extrapolate.
    def plot_with_estimate(
        a_list: list[int], 
        fit: Predictor,
        n_extrapolate: int = 0, 
        title: str = "Observed a(n) and fitted estimate â(n)"
    ) -> None:

        M = len(a_list)
        n_max = M + n_extrapolate
        ns = list(range(1, n_max + 1))

        # compute predictions and bands
        a_hat = []
        lo_band = []
        hi_band = []
        for n in ns:
            hat, lo, hi = fit(n)
            a_hat.append(hat)
            lo_band.append(lo)
            hi_band.append(hi)

        # prepare figure
        plt.figure(figsize=(10, 6))
        # observed points for 1..M
        plt.scatter(range(1, M + 1), a_list, color="tab:blue", label="observed a(n)", zorder=3)
        # fitted curve (solid) and prediction band
        plt.plot(ns, a_hat, color="tab:orange", linewidth=2, label="fitted â(n)")
        plt.fill_between(ns, lo_band, hi_band, color="tab:orange", alpha=0.18, label="approx 95% band")

        # cosmetic
        plt.xlabel("n")
        plt.ylabel("a(n)")
        plt.title(title)
        plt.grid(alpha=0.3)
        plt.legend()
        plt.xlim(1 - 0.5, n_max + 0.5)
        # show integer ticks if small range
        if n_max <= 60:
            plt.xticks(range(1, n_max + 1))
        plt.tight_layout()
        plt.show()

    # plot including extrapolation 
    plot_with_estimate(a_list, fit, n_extrapolate=N//5, title=title)

"""
Computing A390393 a(1)..a(50) with exact rational sorting.
[0, 1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 13, 14, 15, 16, 16, 17, 18, 19, 19, 20, 21, 22, 22, 23, 24, 25, 26, 26, 27, 28, 29, 30, 31, 32, 33, 34, 34, 35, 36, 37, 38, 39, 40, 41, 42]

Fitted parameters:
  s0 = 0.632120558829
  A  = -2.976911
  C  = 4.239175
  sigma (resid std) = 1.299287

Predictions for selected n:
n = 10: a(10) = 8, predicted 9 (95% CI: [6.39, 11.48])
n = 20: a(20) = 16, predicted 17 (95% CI: [14.77, 19.87])
n = 30: a(30) = 24, predicted 25 (95% CI: [22.30, 27.40])
n = 40: a(40) = 33, predicted 32 (95% CI: [29.48, 34.57])
n = 50: a(50) = 42, predicted 39 (95% CI: [36.47, 41.56])
n = 60: a(60) = --, predicted 46 (95% CI: [43.33, 48.42])
n = 70: a(70) = --, predicted 53 (95% CI: [50.11, 55.20])
n = 80: a(80) = --, predicted 59 (95% CI: [56.83, 61.92])
n = 90: a(90) = --, predicted 66 (95% CI: [63.50, 68.59])
n = 100: a(100) = --, predicted 73 (95% CI: [70.14, 75.23])
"""