import numpy as np


def split4(arr):
    arr_left, arr_right = np.hsplit(arr, 2)
    return np.vsplit(arr_left, 2) + np.vsplit(arr_right, 2)


def mult(a, b):
    if np.shape(a)[0] == 1:
        return a * b
    a11, a21, a12, a22 = split4(a)
    b11, b21, b12, b22 = split4(b)
    p1 = mult(a11 + a22, b11 + b22)
    p2 = mult(a21 + a22, b11)
    p3 = mult(a11, b12 - b22)
    p4 = mult(a22, b21 - b11)
    p5 = mult(a11 + a12, b22)
    p6 = mult(a21 - a11, b11 + b12)
    p7 = mult(a12 - a22, b21 + b22)

    c11 = p1 + p4 - p5 + p7
    c12 = p3 + p5
    c21 = p2 + p4
    c22 = p1 - p2 + p3 + p6
    return np.vstack((np.hstack((c11, c12)),
                      np.hstack((c21, c22))))
n = int(input())
n_extended = 1
while n_extended < n:
    n_extended = n_extended * 2
a = np.zeros((n_extended, n_extended), int)
b = np.zeros((n_extended, n_extended), int)
for i in range(n):
    a[i, :n] = list(map(int, input().split()))
for i in range(n):
    b[i, :n] = list(map(int, input().split()))
c = mult(a, b)

for row in c[:n, :n]:
    print(*row)
