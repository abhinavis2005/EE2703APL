def mean(x, axis=0):
    s = []
    if (axis==1):
        for i in range(len(x)):
            sum = 0
            for j in range(len(x[i])): sum+= x[i][j]
            s.append(sum/len(x[i]))
            
    elif (axis==0):
        for i in range(len(x[0])):
            sum = 0
            for j in range(len(x)): sum += x[j][i]
            s.append(sum / len(x))
    return s

x=[[1,2],[3,4], [5,6]]
s1 = mean(x, axis=1)
s2 = [3, 4]
print(s1)
