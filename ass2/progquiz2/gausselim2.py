def gausselim(A,B):
    #nomralize row1 
    #creating an upper traingular matrix

    #number of equatons, varibles
    n = len(A)
    for i in range(n):
        norm = A[i][i]

        for elem_idx in range(n): A[i][elem_idx]/=norm
        B[i]=B[i]/norm

        for j in range(i+1,n): #from i + 1 th row

            norm = A[j][i]
            for elem_idx in range(n):
                A[j][elem_idx] -= A[i][elem_idx]*norm
            B[j] -= B[i]*norm
    
    #back substitution
    
    for i in range(n-2, -1, -1):
        for j in range(i+1, n):
            norm = A[i][j]
            A[i][j] -= A[i][j]
            B[i] -= norm*B[j]

    return B 
A = [ [2,3], [1,-1] ]
B = [6,1/2]
