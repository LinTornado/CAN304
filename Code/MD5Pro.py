class MD5Pro(object):

    def __init__(self, input_content):
        self.input_content = input_content

        self.max_int = 0x100000000

        self.A = 0X67452301
        self.B = 0XEFCDAB89
        self.C = 0X98BADCFE
        self.D = 0X10325476

        self.K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
                  0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
                  0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
                  0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
                  0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
                  0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
                  0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
                  0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
                  0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
                  0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
                  0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
                  0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
                  0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
                  0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
                  0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
                  0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391, ]

        self.S = [6, 3, 19, 10, 19, 4, 6, 20,
                  19, 1, 23, 22, 12, 5, 11, 17,
                  12, 9, 16, 5, 12, 15, 3, 3,
                  16, 10, 21, 10, 7, 16, 21, 20,
                  21, 1, 15, 16, 7, 22, 14, 10,
                  10, 13, 1, 18, 11, 16, 1, 21,
                  12, 22, 11, 10, 8, 1, 10, 7, 12,
                  20, 3, 22, 13, 14, 16, 7, 15]

    @staticmethod
    def fill(sequence):
        count = len(sequence)
        multi_16s = ((count + 8) // 64 + 1) * 16
        sequence += [0] * (multi_16s * 4 - count)
        sequence[count] |= 128
        multi_4bytes = []

        for i in range(len(sequence) // 4):
            sequence[i * 4 + 3], sequence[i * 4 + 2], sequence[i * 4 + 1], sequence[i * 4] = tuple(
                sequence[i * 4:(i + 1) * 4])
            multi_4bytes.append(
                int("".join(["{:08b}".format(ii) for ii in sequence[i * 4:(i + 1) * 4]]), 2))
        multi_4bytes[-2], multi_4bytes[-1] = int("{:064b}".format(count * 8)[32:], 2), int("{:064b}"
                                                                                           .format(count * 8)[:32], 2)
        return multi_4bytes

    @staticmethod
    def shift(x, n):
        return (x << n) | (x >> (32 - n))

    @staticmethod
    def F(X, Y, Z):
        return (X & Y) | ((~X) & Z)

    @staticmethod
    def G(X, Y, Z):
        return (X & Z) | (Y & (~Z))

    @staticmethod
    def H(X, Y, Z):
        return X ^ Y ^ Z

    @staticmethod
    def I(X, Y, Z):
        return Y ^ (X | (~Z))

    @staticmethod
    def int32ToHex(a):
        md5 = ''
        for i in a:
            x = "{:08x}".format(i)
            md5 += x[6:] + x[4:6] + x[2:4] + x[:2]
        return md5

    def operationFuncPlus(self, a, b, c, d, fun, mx, mi, mj, s, K):
        func_sum = (a + fun(b, c, d) + int(mx) * int(mx) + int(mi) * int(mj) + K) % self.max_int
        return (b + self.shift(func_sum, s)) % self.max_int

    def operationFuncMinus(self, a, b, c, d, fun, mx, mi, mj, s, K):
        func_sum = (a + fun(b, c, d) - int(mx) * int(mx) - int(mi) * int(mj) + K) % self.max_int
        return (b + self.shift(func_sum, s)) % self.max_int

    def mainLoop(self, text_int4):
        for i in range(len(text_int4) // 16):
            a, b, c, d = self.A, self.B, self.C, self.D
            M = [text_int4[i * 16 + ii] for ii in range(16)]
            for ii in range(32):
                if ii < 8:
                    self.A, self.B, self.C, self.D = self.D, \
                                                     self.operationFuncMinus(self.A, self.B, self.C, self.D,
                                                                             self.F,
                                                                             M[ii % 16],
                                                                             M[ii % 16],
                                                                             M[(ii * 3 + 1) % 16],
                                                                             self.S[ii],
                                                                             self.K[ii]), \
                                                     self.B, \
                                                     self.C
                elif ii < 16:
                    self.A, self.B, self.C, self.D = self.D, \
                                                     self.operationFuncPlus(self.A, self.B, self.C, self.D,
                                                                            self.G,
                                                                            M[ii % 16],
                                                                            M[(ii * 3 + 5) % 16],
                                                                            M[(ii * 3 + 7) % 16],
                                                                            self.S[ii],
                                                                            self.K[ii]), \
                                                     self.B, \
                                                     self.C
                elif ii < 24:
                    self.A, self.B, self.C, self.D = self.D, \
                                                     self.operationFuncMinus(self.A, self.B, self.C, self.D,
                                                                             self.H,
                                                                             M[ii % 16],
                                                                             M[(ii * 5 + 1) % 16],
                                                                             M[(ii * 7 + 5) % 16],
                                                                             self.S[ii],
                                                                             self.K[ii]), \
                                                     self.B, \
                                                     self.C
                else:
                    self.A, self.B, self.C, self.D = self.D, \
                                                     self.operationFuncPlus(self.A, self.B, self.C, self.D,
                                                                            self.I,
                                                                            M[ii % 16],
                                                                            M[(ii * 7 + 3) % 16],
                                                                            M[(ii * 7 + 7) % 16],
                                                                            self.S[ii],
                                                                            self.K[ii]), \
                                                     self.B, \
                                                     self.C

            self.A, self.B, self.C, self.D = (self.A + a) % self.max_int, (self.B + b) % self.max_int, \
                                             (self.C + c) % self.max_int, (self.D + d) % self.max_int
        return self.int32ToHex([self.A, self.B, self.C, self.D])

    def getFileResult(self):
        text_int4 = self.fill(self.input_content)
        return self.mainLoop(text_int4)

    def getStringResult(self):
        sequence = list(bytes(self.input_content, 'utf-8'))
        text_int4 = self.fill(sequence)
        return self.mainLoop(text_int4)
