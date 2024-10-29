import math
from collections import Counter

print('-'*40)
u = int(input("Enter the number of elements: "))
P = list(map(int,input("Enter elements (5 1 1 ..): ").strip().split()))[:u]
print("The Pruffer number is: ",P)

n = len(P)+2
j = []
i = 0

for x in range(1,n+1):
    if x in P:
        counts = Counter(P)
        h = counts[x]
    else:
        h = 0
    j.append(h+1)

print('-'*40)
print(j)
print('Edge of the tree is: ({},{})'.format(j.index(min(j))+1,P[i]))

while True:
    a=j.index(min(j))
    j[a]=j[a]-1
    
    for x in j:
        if x==0:
            l=j.index(x)
            j[l]=math.inf

    j[P[i]-1]=j[P[i]-1]-1

    for x in j:
        if x==0:
            l=j.index(x)
            j[l]=math.inf

    print(j)
    if i < len(P)-1:
        print('Edge of the tree is: ({},{})'.format(j.index(min(j))+1,P[i+1]))

    else:
        print('Edge of the tree is: ({},{})'.format(j.index(1)+1,j.index(1, j.index(1)+1, len(j))+1))

    if len(P) == j.count(math.inf):
        break
    i += 1

print('-'*40)








