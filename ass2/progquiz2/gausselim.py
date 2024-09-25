def gausselim(A, B):
    # Normalize row 1
    norm = A[0][0]
    for i in range(len(A[0])): A[0][i] /= norm
    B[0] = B[0]/norm
    
    # Eliminate row 2 - A[1] 
    norm = A[1][0] / A[0][0]
    for i in range(len(A[1])): A[1][i] = A[1][i] - A[0][i] * norm
    B[1] = B[1] - B[0] * norm

    # Normalize row 2 - B[1] will now contain the solution for x2
    norm = A[1][1]
    for i in range(len(A[1])): A[1][i] = A[1][i] / norm
    B[1] = B[1] / norm

    # Sub back and solve for B[0] <-> x1
    # This can be seen as eliminating A[0][1]
    norm = A[0][1] / A[0][0]
    # note that len(A) will give number of rows
    for i in range(len(A)): 
        A[i][1] = A[i][1] - A[i][0] * norm
        B[i] = B[i] - A[i][0] * norm

    return B

A = [ [3,3], [1,-1] ]
B = [12,2]

Bout = gausselim(A, B)
Bexp = [1.5, 1. ]
s = 0
for i in range(len(Bout)):
    s += abs(Bout[i] - Bexp[i])
print(Bout)
print(Bexp)
if s < 0.01:
  print("PASS")
else:
  print("FAIL")
