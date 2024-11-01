import numpy as np

def py_trapz(f, a, b, n):
    stepsize = (b-a)/n
    integral = 0
    for i in range(n):
        start = a+stepsize*i
        end = start+stepsize
        integral += (f(start)+f(end))*stepsize/2
    return integral


    
if __name__ == "__main__":
    value = py_trapz(lambda x: x*x , 0, 1, 1000000)
    print(f"Integral x^2 from 0 to 1 is {value}")
    value = py_trapz(np.sin, 0, np.pi, 1000000)

    print(f"Integral sinx from 0 to pi is {value}")
    value = py_trapz(np.exp, 0, 1, 1000000)
    print(f"Integral e^x from 0 to 1 is {value}")
    value = py_trapz(lambda x: 1/x,  1, 2, 1000000)
    print(f"Integral 1/x from 1 to 2 is {value}")

