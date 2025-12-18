// knights.cpp
// Count undirected Hamiltonian knight paths on k x n chessboards.
// See OEIS A390833.
// Peter Luschny, December 2025

#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using u64 = unsigned long long;

// Knight neighbor masks
vector<u64> knight_neighbor_masks(int k, int n) {
    static const int moves[8][2] = {
        {1,2},{1,-2},{-1,2},{-1,-2},
        {2,1},{2,-1},{-2,1},{-2,-1}
    };
    int V = k*n;
    vector<u64> masks(V, 0ULL);

    for (int r = 0; r < k; r++) {
        for (int c = 0; c < n; c++) {
            int u = r*n + c;
            u64 m = 0ULL;
            for (auto &mv : moves) {
                int rr = r + mv[0], cc = c + mv[1];
                if (0 <= rr && rr < k && 0 <= cc && cc < n) {
                    int v = rr*n + cc;
                    m |= (1ULL << v);
                }
            }
            masks[u] = m;
        }
    }
    return masks;
}

// Connectivity check
bool remaining_connected(u64 rem, const vector<u64>& nbr) {
    if (rem == 0ULL) return true;
    int start = __builtin_ctzll(rem);
    u64 visited = (1ULL << start);
    deque<int> q;
    q.push_back(start);

    while (!q.empty()) {
        int u = q.front(); q.pop_front();
        u64 nb = nbr[u] & rem;
        while (nb) {
            u64 b = nb & -nb;
            int v = __builtin_ctzll(b);
            nb ^= b;
            if (!(visited & (1ULL << v))) {
                visited |= (1ULL << v);
                q.push_back(v);
            }
        }
    }
    return (visited & rem) == rem;
}

// DFS
u64 dfs(int current,
        u64 visited,
        const vector<u64>& nbr,
        u64 ALL_MASK)
{
    if (visited == ALL_MASK)
        return 1;

    u64 total = 0;
    u64 cand = nbr[current] & ~visited;
    if (!cand) return 0;

    vector<pair<int,int>> order;
    u64 tmp = cand;
    while (tmp) {
        u64 b = tmp & -tmp;
        int v = __builtin_ctzll(b);
        tmp ^= b;
        int rem_deg = __builtin_popcountll(nbr[v] & ~visited);
        order.emplace_back(rem_deg, v);
    }
    sort(order.begin(), order.end());

    for (auto &p : order) {
        int v = p.second;
        u64 new_mask = visited | (1ULL << v);
        u64 rem = ALL_MASK & ~new_mask;
        if (rem && !remaining_connected(rem, nbr))
            continue;
        total += dfs(v, new_mask, nbr, ALL_MASK);
    }
    return total;
}

// Symmetry-reduced start vertices (D2)
bool in_fundamental_domain(int r, int c, int k, int n) {
    if (r < k/2) return true;
    if (r == k/2 && c < n/2) return true;
    return false;
}

// Main counting function
u64 knight_hamiltonian_paths(int k, int n) {
    if (k > n) std::swap(k, n); // symmetry

    vector<u64> nbr = knight_neighbor_masks(k, n);
    int V = k*n;
    u64 ALL_MASK = (V == 64 ? ~0ULL : ((1ULL << V) - 1ULL));
    u64 total = 0;

    #pragma omp parallel for reduction(+:total) schedule(dynamic)
    for (int r = 0; r < k; r++) {
        for (int c = 0; c < n; c++) {
            if (!in_fundamental_domain(r, c, k, n)) continue;

            int s = r*n + c;
            total += dfs(s, (1ULL << s), nbr, ALL_MASK);
        }
    }
    return total; // symmetry-reduced and canonical
}

int main() {
    int k = 4;
    for (int n = 1; n < 6; n++) {
        u64 c = knight_hamiltonian_paths(k, n);
        cout << "A(" << k << "," << n << ") = " << c << "\n";
    }
}


/*
sudo pacman -Syu
sudo pacman -S gcc clang make cmake libomp
g++ -O3 -march=native -fopenmp -std=c++17 knights.cpp -o knights
./knights
*/
