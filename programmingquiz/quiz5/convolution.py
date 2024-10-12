"""

"""
def convolve(A, B):
    C = []
    for n in range(len(B)+len(A)-1):
        sum = 0
        for k in range(len(A)):
            h_index = n - k 
            if h_index < 0 or h_index >= len(B) :
                continue
            else:
                sum += B[h_index]*A[k]
        C.append(sum)
    return C 
    
def pr_help(l):
    return ",".join(map(str, map(float, l)))

print(convolve([3,2,5,6], [1,2,4]))