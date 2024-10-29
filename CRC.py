s="10011101"
b="1011"
a=s
a=a+3*'0'
print(a)

while True:
    c=len(a)-len(b)
    if len(b) < len(a):
        b=b+c*'0'
    print(b)
    print(len(a)*'-')
    y=int(a,2) ^ int(b,2)
    if len(b) >= len(a):
        b=b.rstrip('0')
    a=format(y,'b')
    print(a)
    if len(a) <= 3:
        break

if len(a) < 3:
    e=3-len(a)
    z=e*'0'+a
else:
    z=a

print("z je:",z)
v=s+z
print("v je:",v)
ch='10011101011'
print("ch je:",ch)

while True:
    c=len(ch)-len(b)
    if len(b) < len(ch):
        b=b+c*'0'
    print(b)
    print(len(ch)*'-')
    y=int(ch,2) ^ int(b,2)
    if len(b) >= len(ch):
        b=b.rstrip('0')
    ch=format(y,'b')
    print(ch)
    if len(ch) <= 3:
        break

print('Tady zaciname:')
i=len(b)-1
h='1'+i*'0'

while True:
    # if ch == '100':
    #     print('na pozici 3 byla chyba')
    #     break
    # elif ch == '10':
    #     print('na pozici 2 byla chyba')
    #     break
    # elif ch == '1':
    #     print('na pozici 1 byla chyba')
    #     break
    print(h)
    c=len(h)-len(b)
    if len(b) < len(h):
        b=b+c*'0'
    print(b)
    print(len(h)*'-')
    y=int(h,2) ^ int(b,2)
    if len(b) >= len(h):
        b=b.rstrip('0')
    h=format(y,'b')
    print(h)
    if h == ch:
        print('na pozici {} byla chyba'.format(i+1))
        break
    if i == len(v)-1:
        print('prenos bez chyby')
        break
    if len(h) <= 3:
        i += 1
        h='1'+i*'0'

