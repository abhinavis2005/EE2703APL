def subsetsum(L,S):
    for i in range(len(L)):
        sum = 0
        for j in range(i, len(L)):
            sum += L[j]
            if sum == S:
                return (i,j)
            elif sum > S:
                break
    return (-1,-1)

