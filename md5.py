#!/usr/bin/env python3

import math
import argparse

class MD5Hash:
    def __init__(self, A, B, C, D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.digest = A + (B << 32) + (C << 64) + (D << 96)
        self.hexdigest = self.digest.to_bytes(16, 'little').hex()

table = [int(abs(math.sin(i+1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]

def pad(msg):
    bit_length = len(msg) * 8
    msg += bytes([0x80])
    while len(msg) % 64 != 56:
        msg += bytes([0])
    msg += bit_length.to_bytes(8, 'little')
    return msg

def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

def rotate_left(x, n):
    x &= 0xFFFFFFFF
    return (x << n | x >> (32 - n)) & 0xFFFFFFFF

def op(a, b, c, d, k, s, i, f, x):
    a = b + rotate_left(a + f(b, c, d) + x[k] + table[i-1], s)
    return a & 0xFFFFFFFF

def md5(msg):
    msg = pad(msg)
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476
    for i in range(len(msg)//64):
        X = []
        for j in range(16):
            offset = 4 * (i * 16 + j)
            word = msg[offset: offset + 4]
            X.append(int.from_bytes(word, 'little'))
        AA = A
        BB = B
        CC = C
        DD = D
        # Round 1
        A = op(A, B, C, D, 0, 7, 1, F, X)
        D = op(D, A, B, C, 1, 12, 2, F, X)
        C = op(C, D, A, B, 2, 17, 3, F, X)
        B = op(B, C, D, A, 3, 22, 4, F, X)
        A = op(A, B, C, D, 4, 7, 5, F, X)
        D = op(D, A, B, C, 5, 12, 6, F, X)
        C = op(C, D, A, B, 6, 17, 7, F, X)
        B = op(B, C, D, A, 7, 22, 8, F, X)
        A = op(A, B, C, D, 8, 7, 9, F, X)
        D = op(D, A, B, C, 9, 12, 10, F, X)
        C = op(C, D, A, B, 10, 17, 11, F, X)
        B = op(B, C, D, A, 11, 22, 12, F, X)
        A = op(A, B, C, D, 12, 7, 13, F, X)
        D = op(D, A, B, C, 13, 12, 14, F, X)
        C = op(C, D, A, B, 14, 17, 15, F, X)
        B = op(B, C, D, A, 15, 22, 16, F, X)
        # Round 2
        A = op(A, B, C, D, 1, 5, 17, G, X)
        D = op(D, A, B, C, 6, 9, 18, G, X)
        C = op(C, D, A, B, 11, 14, 19, G, X)
        B = op(B, C, D, A, 0, 20, 20, G, X)
        A = op(A, B, C, D, 5, 5, 21, G, X)
        D = op(D, A, B, C, 10, 9, 22, G, X)
        C = op(C, D, A, B, 15, 14, 23, G, X)
        B = op(B, C, D, A, 4, 20, 24, G, X)
        A = op(A, B, C, D, 9, 5, 25, G, X)
        D = op(D, A, B, C, 14, 9, 26, G, X)
        C = op(C, D, A, B, 3, 14, 27, G, X)
        B = op(B, C, D, A, 8, 20, 28, G, X)
        A = op(A, B, C, D, 13, 5, 29, G, X)
        D = op(D, A, B, C, 2, 9, 30, G, X)
        C = op(C, D, A, B, 7, 14, 31, G, X)
        B = op(B, C, D, A, 12, 20, 32, G, X)
        # Round 3
        A = op(A, B, C, D, 5, 4, 33, H, X)
        D = op(D, A, B, C, 8, 11, 34, H, X)
        C = op(C, D, A, B, 11, 16, 35, H, X)
        B = op(B, C, D, A, 14, 23, 36, H, X)
        A = op(A, B, C, D, 1, 4, 37, H, X)
        D = op(D, A, B, C, 4, 11, 38, H, X)
        C = op(C, D, A, B, 7, 16, 39, H, X)
        B = op(B, C, D, A, 10, 23, 40, H, X)
        A = op(A, B, C, D, 13, 4, 41, H, X)
        D = op(D, A, B, C, 0, 11, 42, H, X)
        C = op(C, D, A, B, 3, 16, 43, H, X)
        B = op(B, C, D, A, 6, 23, 44, H, X)
        A = op(A, B, C, D, 9, 4, 45, H, X)
        D = op(D, A, B, C, 12, 11, 46, H, X)
        C = op(C, D, A, B, 15, 16, 47, H, X)
        B = op(B, C, D, A, 2, 23, 48, H, X)
        # Round 4
        A = op(A, B, C, D, 0, 6, 49, I, X)
        D = op(D, A, B, C, 7, 10, 50, I, X)
        C = op(C, D, A, B, 14, 15, 51, I, X)
        B = op(B, C, D, A, 5, 21, 52, I, X)
        A = op(A, B, C, D, 12, 6, 53, I, X)
        D = op(D, A, B, C, 3, 10, 54, I, X)
        C = op(C, D, A, B, 10, 15, 55, I, X)
        B = op(B, C, D, A, 1, 21, 56, I, X)
        A = op(A, B, C, D, 8, 6, 57, I, X)
        D = op(D, A, B, C, 15, 10, 58, I, X)
        C = op(C, D, A, B, 6, 15, 59, I, X)
        B = op(B, C, D, A, 13, 21, 60, I, X)
        A = op(A, B, C, D, 4, 6, 61, I, X)
        D = op(D, A, B, C, 11, 10, 62, I, X)
        C = op(C, D, A, B, 2, 15, 63, I, X)
        B = op(B, C, D, A, 9, 21, 64, I, X)
        # Four additions
        A = (A + AA) & 0xFFFFFFFF  
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF
    return MD5Hash(A, B, C, D)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='md5.py', description='MD5 Hashing Algorithm')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('message', nargs='?', type=str)
    group.add_argument('-i', '--inputfile', type=str) 
    parser.add_argument('-o', '--outputfile', type=str)
    parser.add_argument('-c', '--compare', action='store_true')
    args = parser.parse_args()
    if args.message:
        msg = args.message.encode('utf-8')
    elif args.inputfile:
        with open(args.inputfile, 'rb') as file:
            msg = file.read()
    hash = md5(msg)
    print(hash.hexdigest)
    if args.outputfile:
        with open(args.outputfile, 'w') as file:
            file.write(hash.hexdigest)
    if args.compare:
        import hashlib
        hash = hashlib.md5(msg)
        print(hash.hexdigest(), '(hashlib)')
