import math
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

prime_n=[]

def Sieve(n):
    prime = [True for i in range(n+1)]
    p = 2
    while(p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    c = 0
 
    for p in range(2, n):
        if prime[p]:
            prime_n.append(p)
            c += 1
    return c

print("Input number of natural numbers:")
amount = int(input())
t0 = time.time()
c = Sieve(amount)
print("Total prime numbers in range:", c)
t1 = time.time()
print("Time required:", t1 - t0)

d = [0 for i in range(len(prime_n))]
print("Input number which will shape our graph (2;10):")
w = int(input())
i= 0
while i < len(d)//w:
    for j in range(0, len(prime_n)//w):  
        d[i] = 0.001 * prime_n[j] - 0.001 * prime_n[len(prime_n)//w]
        i += 1

def get_coordinate(num):
    return num * np.cos(num), num * np.sin(num), d

prime_n = np.array(list(prime_n))
x, y, z = get_coordinate(prime_n)

plt.style.use('dark_background')
fig = plt.figure(figsize=(8, 8))
ax = plt.axes(projection ='3d')
plt.axis("off")
ax.scatter(x, y, z, s=1)
plt.show()


