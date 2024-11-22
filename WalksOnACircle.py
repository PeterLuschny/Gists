# SageMath

def isWalk(m, S) :
    vec = [0]*m
    max = len(S) // m
    dir = 0
    os = S[0]
    for s in S :
        if s and os :
            dir += 1
        elif not s and not os :
            dir -=1
        dir %= m
        v = vec[dir] + 1
        vec[dir] = v
        if v > max :
            return False
        os = s
    return True

def WalksOnTheCircle(m, len) :
    count = 0
    for a in range(m, len + 1, m):
        S = [1] * a + [0] * (len - a)
        for c in Permutations(S) :
            if not c[0] : continue
            if isWalk(m, c) : 
                count += 1
                print("".join(map(str, c)))
    return count

WalksOnTheCircle(3, 9)
