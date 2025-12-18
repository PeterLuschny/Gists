// knights.cpp
// Count undirected Hamiltonian knight paths on k x n chessboards.
// See OEIS A390833.
// Peter Luschny, December 2025

#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using u64 = unsigned long long;

// Generate knight-move neighbor masks
vector<u64> knight_neighbor_masks(int k, int n) {
    static const int moves[8][2] = {
        {1,2},{1,-2},{-1,2},{-1,-2},
        {2,1},{2,-1},{-2,1},{-2,-1}
    };
    int V = k * n;
    vector<u64> masks(V, 0ULL);

    for (int r = 0; r < k; r++) {
        for (int c = 0; c < n; c++) {
            int u = r * n + c;
            u64 m = 0ULL;
            for (auto &mv : moves) {
                int rr = r + mv[0], cc = c + mv[1];
                if (0 <= rr && rr < k && 0 <= cc && cc < n) {
                    int v = rr * n + cc;
                    m |= (1ULL << v);
                }
            }
            masks[u] = m;
        }
    }
    return masks;
}

// Connectivity check on remaining vertices
bool remaining_connected(u64 rem, const vector<u64>& nbr) {
    if (rem == 0ULL) return true;

    // find lowest set bit
    int start = __builtin_ctzll(rem);
    u64 visited = (1ULL << start);

    deque<int> q;
    q.push_back(start);

    while (!q.empty()) {
        int u = q.front(); q.pop_front();
        u64 nbrs = nbr[u] & rem;
        while (nbrs) {
            u64 b = nbrs & -nbrs;
            int v = __builtin_ctzll(b);
            nbrs ^= b;
            if (!(visited & (1ULL << v))) {
                visited |= (1ULL << v);
                q.push_back(v);
            }
        }
    }
    return (visited & rem) == rem;
}

// DFS
u64 dfs(int current, u64 visited, const vector<u64>& nbr, u64 ALL_MASK) {
    if (visited == ALL_MASK)
        return 1;

    u64 total = 0;
    u64 cand = nbr[current] & ~visited;
    if (!cand) return 0;

    // Build candidate list with remaining-degree ordering
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

// Count undirected Hamiltonian knight paths
u64 knight_hamiltonian_paths(int k, int n) {
    vector<u64> nbr = knight_neighbor_masks(k, n);
    int V = k * n;
    u64 ALL_MASK = (V == 64 ? ~0ULL : ((1ULL << V) - 1ULL));
    u64 total = 0;

    // Parallelize across start vertices
    #pragma omp parallel for reduction(+:total) schedule(dynamic)
    for (int s = 0; s < V; s++) {
        total += dfs(s, (1ULL << s), nbr, ALL_MASK);
    }

    // Each undirected path counted twice
    return total / 2;
}

int main() {
    int k = 9;
    // [9]  0, 0, 560, 189688, 264895640, 1770631206422, ...
    for (int n = 1; n < 5; n++) {
        u64 c = knight_hamiltonian_paths(k, n);
        cout << "A(" << k << ", " << n << ") = " << c << "\n";
    }
    return 0;
}

/*
sudo pacman -Syu
sudo pacman -S gcc clang make cmake libomp
g++ -O3 -march=native -fopenmp -std=c++17 knights.cpp -o knights
./knights
*/
