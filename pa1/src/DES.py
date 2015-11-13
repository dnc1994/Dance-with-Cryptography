import random
import binascii

class DES(object):

    # Initial permutation for subkey generation (IPC)
    __ipc = [
        56, 48, 40, 32, 24, 16,  8,
         0, 57, 49, 41, 33, 25, 17,
         9,  1, 58, 50, 42, 34, 26,
        18, 10,  2, 59, 51, 43, 35,
        62, 54, 46, 38, 30, 22, 14,
         6, 61, 53, 45, 37, 29, 21,
        13,  5, 60, 52, 44, 36, 28,
        20, 12,  4, 27, 19, 11,  3
    ]

    # Left rotation for subkey generation (LS)
    __ls = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    ]

    # Final permutation for subkey generation (FPC)
    __fpc = [
        13, 16, 10, 23,  0,  4,
         2, 27, 14,  5, 20,  9,
        22, 18, 11,  3, 25,  7,
        15,  6, 26, 19, 12,  1,
        40, 51, 30, 36, 46, 54,
        29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52,
        45, 41, 49, 35, 28, 31
    ]

    # Initial permutation (IP)
    __ip = [
        57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8,  0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]

    # Expansion table (E)
    __et = [
        31,  0,  1,  2,  3,  4,
         3,  4,  5,  6,  7,  8,
         7,  8,  9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31,  0
    ]

    # S-boxes
    __sbox = [
        # S1
        [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
          0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
          4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
         15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],

        # S2
        [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
          3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
          0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
         13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],

        # S3
        [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
         13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
         13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
          1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12],

        # S4
        [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
         13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
         10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
          3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],

        # S5
        [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
         14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
          4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
         11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3],

        # S6
        [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
         10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
          9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
          4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],

        # S7
        [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
         13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
          1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
          6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],

        # S8
        [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
          1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
          7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
          2,  1, 14,  7,  4, 10,  8, 13, 15,  12, 9,  0,  3,  5,  6, 11],
    ]

    # Post S-boxes permutation (P)
    __psp = [
        15,  6, 19, 20, 28, 11,
        27, 16,  0, 14, 22, 25,
         4, 17, 30,  9,  1,  7,
        23, 13, 31, 26,  2,  8,
        18, 12, 29,  5, 21, 10,
         3, 24
    ]

    # Final permutation (IP^-1)
    __fp = [
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25,
        32,  0, 40,  8, 48, 16, 56, 24
    ]
    
    # Cryption modes
    ENC = 0
    DEC = 1
    
    # Cryption rounds
    ROUNDS = 6
    
    def __init__(self, key):
        self.K = [[0] * 48] * DES.ROUNDS
        self.L = []
        self.R = []
        self.C = []
        self.set_key(key)
        self.set_iv(self.gen_bits(64))
        
    def get_key(self):
        return self.__key
        
    def set_key(self, key):
        self.__key = self.__string_to_bits(key)
        self.K = [[0] * 48] * DES.ROUNDS
        self.__generate_subkeys()

    def get_iv(self):
        return self.__iv
        
    def set_iv(self, iv):
        self.__iv = self.__string_to_bits(iv)
    
    def __string_to_bits(self, x):
        return map(int, list(x))
        
    def __bits_to_string(self, x):
        return ''.join(map(str, x))
        
    def __listxor(self, a, b):
        return map(lambda x, y: x ^ y, a, b)
        
    def __permutate(self, block, table):
        return map(lambda x: block[x], table)
    
    # Get the padding char(in binary) according to padding length
    def __get_pad(self, plen):
        pch = bin(int(binascii.hexlify(chr(plen)), 16))[2:]
        return '0' * (8 - len(pch)) + pch
    
    # Recover padding length according to the padding char
    def __read_pad(self, pstr):
        return int('0b' + pstr, 2)
        
    def __pad(self, data):
        plen = 8 - (len(data) % 64) / 8
        return data + self.__get_pad(plen) * plen
        
    def __unpad(self, data):
        plen = self.__read_pad(data[-8:])
        return data[:-(plen * 8)] 
    
    def __generate_subkeys(self):
        key = self.__permutate(self.get_key(), DES.__ipc)
        self.L, self.R = key[:28], key[28:]
        
        for i in range(DES.ROUNDS):
                
            for j in range(DES.__ls[i]):
                self.L.append(self.L[0])
                del self.L[0]
                self.R.append(self.R[0])
                del self.R[0]
                
            self.K[i] = self.__permutate(self.L + self.R, DES.__fpc)
    
    # Implementation of single-block crypting
    def __crypt(self, block, crypt_type):   
        block = self.__permutate(block, DES.__ip)
        self.L, self.R = block[:32], block[32:]
        round_no, round_delta = {DES.ENC: (0, 1), DES.DEC: (DES.ROUNDS-1, -1)}[crypt_type]
        
        for i in range(DES.ROUNDS):
            # make a copy of R[i-1] -> L[i]
            old_R = self.R[:]
            
            # -> R[i]
            self.R = self.__permutate(self.R, self.__et)
            
            # Xor R[i-1] with K[i]
            self.R = self.__listxor(self.R, self.K[round_no])
            
            B = [self.R[x*6:(x+1)*6] for x in range(8)]
            
            new_B = [0] * 32        
            for j in range(8):
                # S-box mapping
                l = (B[j][0] << 1) + B[j][5]
                n = (B[j][1] << 3) + (B[j][2] << 2) + (B[j][3] << 1) + B[j][4]
                v = self.__sbox[j][(l << 4) + n]
                
                # Convert to bits
                new_B[j*4+0] = (v & 8) >> 3
                new_B[j*4+1] = (v & 4) >> 2
                new_B[j*4+2] = (v & 2) >> 1
                new_B[j*4+3] = (v & 1) >> 0
            
            # Post S-box permutation
            self.R = self.__permutate(new_B, DES.__psp)
            
            # Xor with L[i-1]
            self.R = self.__listxor(self.L, self.R)
            self.L = old_R
            
            round_no += round_delta
        
        # Final permutation
        self.C = self.__permutate(self.R + self.L, DES.__fp)
        
        return self.C
    
    # Interface for actual crypting
    
    
    def encrypt(self, data_string):
        # Since input is binary string, its length must be of multiple of 8
        assert(len(data_string) % 8 == 0)
        
        # Append IV before the data
        data_string = self.__bits_to_string(self.get_iv()) + data_string
        # Apply padding (using PKCS5 mode)
        data_string = self.__pad(data_string)
        
        data = self.__string_to_bits(data_string)
        result = []
        first_block = True
        
        # Start crypting
        for i in range(0, len(data), 64):         
            block = data[i:i+64]   
            
            if not first_block:
                block = self.__listxor(iv, block)             
            crypted_block = self.__crypt(block, DES.ENC)          
            iv = crypted_block          
            
            result += crypted_block 
            if first_block:
                iv = block
                first_block = False
                
        result = self.__bits_to_string(result)    
        return result
        
    def decrypt(self, data_string):
        # Since input is binary string, its length must be of multiple of 8
        assert(len(data_string) % 8 == 0)
        
        data = self.__string_to_bits(data_string)
        result = []
        first_block = True
        
        # Start crypting
        for i in range(0, len(data), 64):         
            block = data[i:i+64]   
            
            crypted_block = self.__crypt(block, DES.DEC)           
            if not first_block:
                crypted_block = self.__listxor(iv, crypted_block)
            iv = block                
            
            result += crypted_block
            if first_block:
                iv = crypted_block
                first_block = False
        
        result = self.__bits_to_string(result)
        # Apply unpadding
        result = self.__unpad(result)
        # Remove IV from the result
        return result[64:]

    def gen_bits(self, length):
        return ''.join([random.choice(['0', '1']) for _ in range(length)])

# Test utilities        
def gen_bits(l):
    return ''.join([random.choice(['0', '1']) for _ in range(l)])
        
def string_to_bits(x):
    return map(int, list(x))    
            
def bits_to_string(x):
    return ''.join(map(str, x))

def get_pad(plen):
    pch = bin(int(binascii.hexlify(chr(plen)), 16))[2:]
    return '0' * (8 - len(pch)) + pch

def read_pad(pstr):
    return int('0b' + pstr, 2)
    
def pad(data):
    plen = 8 - (len(data) % 64) / 8
    return data + get_pad(plen) * plen
        
def unpad(data):
    plen = read_pad(data[-8:])
    return data[:-(plen * 8)]    

def test():
    key = gen_bits(64)
    des = DES(key=key)
    pt_len_list = [56, 64, 120, 128, 800]
    for pt_len in pt_len_list:
        pt = gen_bits(pt_len)
        ct = des.encrypt(pt)
        pt2 = des.decrypt(ct)
        assert pt == pt2
    
if __name__ == '__main__': 

    test()