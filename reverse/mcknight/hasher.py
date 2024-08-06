import sys
import lzma

FLAG_LEN = 17

nums = [203, 99, 1, 219, 19, 54, 46, 170, 180, 120, 22, 249, 236, 87, 27, 223, 81, 252, 232, 66, 241, 61, 235, 40, 217, 74, 145, 196, 7, 131, 75, 56, 105, 134, 48, 49, 149, 127, 73, 65, 70, 45, 53, 121, 198, 193, 207, 138, 32, 0, 132, 122, 10, 210, 189, 44, 164, 25, 166, 195, 5, 47, 157, 20, 119, 247, 199, 97, 152, 14, 148, 124, 123, 36, 30, 76, 58, 192, 110, 178, 175, 202, 155, 23, 50, 168, 156, 106, 84, 186, 197, 95, 140, 79, 43, 15, 244, 125, 205, 3, 234, 212, 13, 182, 233, 255, 71, 163, 254, 150, 26, 90, 33, 109, 183, 37, 92, 248, 167, 9, 173, 91, 107, 133, 253, 88, 31, 220, 153, 83, 55, 141, 62, 101, 28, 242, 112, 52, 89, 6, 17, 135, 211, 181, 39, 208, 209, 85, 158, 69, 137, 229, 93, 231, 226, 41, 114, 42, 215, 108, 68, 77, 18, 177, 246, 191, 64, 86, 190, 218, 102, 185, 160, 142, 172, 171, 237, 238, 245, 59, 146, 213, 151, 113, 139, 144, 230, 143, 98, 8, 194, 29, 221, 115, 34, 82, 11, 57, 78, 214, 12, 80, 251, 111, 184, 162, 224, 201, 4, 206, 204, 227, 38, 169, 130, 67, 116, 128, 35, 187, 51, 216, 126, 96, 147, 72, 100, 174, 103, 118, 239, 161, 188, 129, 240, 222, 16, 24, 243, 228, 165, 2, 200, 225, 104, 60, 21, 159, 117, 94, 176, 154, 250, 63, 179, 136]

def generator(cnt):
    coeffs = []
    for i in range(cnt):
        aux = []
        for j in range(cnt):
            aux.append(nums[((i + j) * 1337) % 256])
        coeffs.append(aux)

    return coeffs

coeffs = generator(FLAG_LEN)


def calc_line(k, password):
    rez = 0
    for i in range(len(password)):
        rez += password[i] * coeffs[k][i]
    return rez



def hash(password):
    password = password.encode()

    rez = []
    for i in range(FLAG_LEN):
        rez.append(calc_line(i, password))

    final = []
    for k in range(FLAG_LEN):
        aux = 0
        for i in range(FLAG_LEN):
            aux += coeffs[i][i] * (rez[k] ** i)
        # print(aux)
        # exit()
        final.append(aux)

    data = 'X'.join([str(i) for i in final])
    data = lzma.compress(data.encode())

    return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 hasher.py <password>")
        sys.exit(1)
    password = sys.argv[1]
    f = open("flag.tfc", "wb")
    f.write(hash(password))
    f.close()