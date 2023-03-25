a = int("123")
b = int("456")
n = str(a)
m = str(b)
n1 = n[::-1]
m1 = m[::-1]
x = int(n1)
y = int(m1)
if x > 1:
    for i in range(2, x):
        if (x % i) == 0:
            p = 0
            break
        else:
            p = 1
else:
    p = 0
if y > 1:
    for j in range(2, y):
        if (y % j) == 0:
            q = 0
            break
        else:
            q = 1
else:
    q = 0
if p == 1 and q == 1:
    g = x + y
    print(g)
elif p = 1 or q = 1:
    h = a + b
    print(h)
else:
    print(a * b)
