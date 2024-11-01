
def d(n):
    sum = 1
    i = 2
    while i*i < n:
        if n%i == 0:
            sum += i
            sum += n/i
        i+=1
    return int(sum)
def amicable(n1, n2):
    if d(n1) == n2 and d(n2) == n1 and n1 != n2:
        return True
    else:
        return False
def amsum(N):
    ds={}
    sum = 0
    for i in range(N):
        if i not in ds.keys():
            #i = n1
            ds[i] = d(i)
            #d(n1) = n2 and d(n2) = n1
            ds[d(i)] = d(d(i))
            if (ds[d(i)]==i and ds[i]!=i):
                sum += i + ds[i]
    return sum
        
    
print(d(6))
