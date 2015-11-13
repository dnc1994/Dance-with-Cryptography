import random


# Miller-Rabin test for odd-number n(n > 3), c = confidence(the number of integer a used in the test)        
def miller_rabin(n, c):

    def mr_test(a, n, m, k):  
        b = pow(a, m, n)
        if b == 1:
            return True
        else:
            for j in range(k-1):
                if b == n-1:
                    return True
                b = (b * b) % n
            return b == n-1
        
    m, k = n-1, 0
    while m % 2 == 0:
        m >>= 1
        k += 1
      
    for i in range(c):
        a = random.randrange(2, n-1)
        if not mr_test(a, n, m, k):
            return False
    return True
    
    
# Euclidean GCD Algorithm    
def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)
 

# Extended GCD Algorithm
def exgcd(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, g = exgcd(b, a%b)
        return y, x - y * (a // b), g


# Calculate multiplicative inverse of a under modulus n, inverse only exists when (a, n) == 1
def multi_inverse(a, n):
    x, y, g = exgcd(a, n)
    return x % n if g == 1 else None
    
        
class RSA(object):
    ENC = 0
    DEC = 1

    def __init__(self, key_length=128, confidence=100):
        self.confidence = confidence
        self.key_length = key_length
        self.__gen_primes()
        self.__gen_keys()      

    # Generate p and q
    def __gen_primes(self):
        while True:
            p = random.getrandbits(self.key_length / 2)
            if miller_rabin(p, self.confidence):
                self.p = p
                break
                    
        while True:
            q = random.getrandbits(self.key_length / 2)
            if miller_rabin(q, self.confidence):
                self.q = q
                break

    # Generate modulus, phi and then (d, e) pair as the RSA keys
    def __gen_keys(self):
        self.modulus = self.p * self.q
        # self.phi = (self.p - 1) * (self.q - 1)
        self.phi = self.modulus - self.p - self.q + 1
        
        while True:
            while True:
                e = random.randrange(3, self.phi)
                if gcd(e, self.phi) == 1:
                    self.e = e
                    break
                    
            d = multi_inverse(self.e, self.phi)
            if d:
                self.d = d
                break
            else:
                continue
    
    def encrypt(self, pt, public_key):
        modulus, e = map(self.__binstr_to_num, list(public_key))
        pt = self.__binstr_to_num(pt)
        return self.__num_to_binstr(pow(pt, e, modulus))

    def decrypt(self, ct, private_key):
        modulus, d = map(self.__binstr_to_num, list(private_key))
        ct = self.__binstr_to_num(ct)
        return self.__num_to_binstr(pow(ct, d, modulus))

    def get_p(self):
        assert self.p
        return self.__num_to_binstr(self.p)
    
    def get_q(self):
        assert self.q
        return self.__num_to_binstr(self.q)

    def get_public_key(self):
        assert self.modulus
        assert self.e
        return (self.__num_to_binstr(self.modulus), self.__num_to_binstr(self.e))

    def get_private_key(self):
        assert self.modulus
        assert self.d
        return (self.__num_to_binstr(self.modulus), self.__num_to_binstr(self.d))
    
    def __num_to_binstr(self, num):
        num = bin(num)[2:]
        return '0' * (max(0, self.key_length - len(num))) + num

    def __binstr_to_num(self, binstr):
        return int('0b' + binstr, 2)      
 
 
def test():
    
    def gen_primes(n):
        return filter(lambda x: all(map(lambda p: x % p != 0, range(2, x))), range(2, n))

    def num_to_binstr(num):
        num = bin(num)[2:]
        return '0' * (max(0, 128 - len(num))) + num

    def binstr_to_num(binstr):
        return int('0b' + binstr, 2)  

    # Test Miller-Rabin   
    plist = gen_primes(500)[10:]
    ptruth = [miller_rabin(x, 100) for x in plist]
    assert all(ptruth)   
    print 'Miller-Rabin OK'
    
    # Test key generation
    for i in range(100):
        # print 'test #%d' % (i)
        rsa = RSA()
        modulus, e = rsa.get_public_key()
        modulus, d = rsa.get_private_key()
        assert len(e) == 128
        assert len(d) == 128
        assert binstr_to_num(d) * binstr_to_num(e) % rsa.phi == 1       
    print 'Key Generation OK'
    
    # Test encryption/decryption correctness
    for i in range(100):
        # print 'test #%d' % (i)
        rsa = RSA()
        des_key = num_to_binstr(random.getrandbits(64))
        ct = rsa.encrypt(des_key, rsa.get_public_key())
        pt = rsa.decrypt(ct, rsa.get_private_key())
        assert des_key == pt
    print 'Encryption/Decryption OK'
    

if __name__ == '__main__':
    test()