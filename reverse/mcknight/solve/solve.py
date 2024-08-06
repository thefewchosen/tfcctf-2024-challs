from z3 import *
import sys
import numpy
import lzma

nums = [203, 99, 1, 219, 19, 54, 46, 170, 180, 120, 22, 249, 236, 87, 27, 223, 81, 252, 232, 66, 241, 61, 235, 40, 217, 74, 145, 196, 7, 131, 75, 56, 105, 134, 48, 49, 149, 127, 73, 65, 70, 45, 53, 121, 198, 193, 207, 138, 32, 0, 132, 122, 10, 210, 189, 44, 164, 25, 166, 195, 5, 47, 157, 20, 119, 247, 199, 97, 152, 14, 148, 124, 123, 36, 30, 76, 58, 192, 110, 178, 175, 202, 155, 23, 50, 168, 156, 106, 84, 186, 197, 95, 140, 79, 43, 15, 244, 125, 205, 3, 234, 212, 13, 182, 233, 255, 71, 163, 254, 150, 26, 90, 33, 109, 183, 37, 92, 248, 167, 9, 173, 91, 107, 133, 253, 88, 31, 220, 153, 83, 55, 141, 62, 101, 28, 242, 112, 52, 89, 6, 17, 135, 211, 181, 39, 208, 209, 85, 158, 69, 137, 229, 93, 231, 226, 41, 114, 42, 215, 108, 68, 77, 18, 177, 246, 191, 64, 86, 190, 218, 102, 185, 160, 142, 172, 171, 237, 238, 245, 59, 146, 213, 151, 113, 139, 144, 230, 143, 98, 8, 194, 29, 221, 115, 34, 82, 11, 57, 78, 214, 12, 80, 251, 111, 184, 162, 224, 201, 4, 206, 204, 227, 38, 169, 130, 67, 116, 128, 35, 187, 51, 216, 126, 96, 147, 72, 100, 174, 103, 118, 239, 161, 188, 129, 240, 222, 16, 24, 243, 228, 165, 2, 200, 225, 104, 60, 21, 159, 117, 94, 176, 154, 250, 63, 179, 136]

def generator(cnt):
    coeffs = []
    for i in range(cnt):
        aux = []
        for j in range(cnt):
            aux.append(nums[((i + j) * 1337) % 256])
        coeffs.append(aux)

    return coeffs

coeffs = generator(32)


def calc_line(k, password):
    rez = 0
    for i in range(len(password)):
        rez += password[i] * coeffs[k][i]
    return rez

def pow(a, b):
    rez = a
    for i in range(b - 1):
        rez *= a
    return rez

def hash(password):
    rez = []
    for i in range(32):
        rez.append(calc_line(i, password))

    final = 0
    for i in range(32):
        final += coeffs[i][i] * (pow(rez[i], (i + 1)))

    return final

FLAG_LEN = 17

def test_polynomial(x):
    rez = 0
    for i in range(FLAG_LEN):
        rez += coeffs[i][i] * (x ** i)
    return rez

data = open("flag.tfc", "rb").read()
data = lzma.decompress(data)
data = data.split(b"X")

pol_coeffs = [coeffs[i][i] for i in range(FLAG_LEN)]
print(pol_coeffs)

rez = []

for x in data:
    for i in range(1000000):
        if test_polynomial(i) == int(x):
            rez.append(i)
            break

password = [BitVec("password_%d" % i, 64) for i in range(FLAG_LEN)]

s = Solver()

for i in range(FLAG_LEN):
    s.add(And(password[i] >= 33, password[i] < 128))


for i in range(FLAG_LEN):
    s.add(calc_line(i, password) == rez[i])

while s.check() == sat:
    m = s.model()
    print("".join([chr(m[password[i]].as_long()) for i in range(FLAG_LEN)]))
    s.add(Or([password[i] != m[password[i]] for i in range(FLAG_LEN)]))
# for root in roots: