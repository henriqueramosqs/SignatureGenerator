import random
import sys
import hashlib
import math
import os
sys.setrecursionlimit(1100)

class Mod:

    def __init__(self,num:int,mod:int):
        self.mod = mod
        self.num = num % mod

    def check_compat(self,ot)->bool:
        return isinstance(ot,Mod) and ot.mod==self.mod
    
    def __add__(self,ot):
        if( not self.check_compat(ot)):
            raise ValueError("Números em classes de congruência diferentes")
        
        return Mod((self.num+ot.num)%self.mod,self.mod)
     
    def __sub__(self,ot):
        if( not self.check_compat(ot)):
            raise ValueError("Números em classes de congruência diferentes")
         
        return Mod((self.num-ot.num)%self.mod,self.mod)

    def __mul__(self,ot):
        if( not self.check_compat(ot)):
            raise ValueError("Números em classes de congruência diferentes")
        return Mod((self.num*ot.num)%self.mod,self.mod)
    
    def __pow__(self,exp:int):
        if(exp==0):
            return Mod(1,self.mod)
        ans = self.__pow__(exp>>1)
        ans*=ans
        if(exp%2==1):
            ans*=self
        return ans
    
    def __repr__(self):
        return "("+str(self.num) + ", " + str(self.mod) +")"
    

def mod_inv(a, mod):
    x = 1
    y = 0
    x1 = 0
    y1 = 1
    a1 = a
    b1 = mod
    while (b1):
        q = a1 // b1
        x, x1= x1, x - q * x1
        y, y1 = y1, y - q * y1
        a1, b1 = b1, a1 - q * b1
    return (x % mod + mod) % mod
    

def is_composite(n: int, a: int, d: int, s: int) -> bool:
    x = Mod(a,n)**d

    if x.num == 1 or x.num == n-1:
        return False
    
    for _ in range(s - 1):
        x**=2
        if x.num == n-1:
            return False
    return True

def is_prime(n:int, iter:int=10)->bool:

    if(n < 4):
        return n == 2 or n == 3

    s = 0
    d = n - 1

    while((d & 1) == 0):
        d >>= 1
        s+=1

    for _ in range(iter):
        a = random.randint(2, n - 2)
        if is_composite(n, a, d, s):
            return False
        
    return True

def gen_prime(bits:int=1024):

    while True:
        n = random.getrandbits(bits) | 1
        if is_prime(n):
            return n

def gen_d(fi_n:int):
    while True:
        d = random.randint(1,fi_n)
        if math.gcd(d,fi_n):
            return d

def mgf(seed,len):
    h_len = hashlib.sha256().digest_size
    if len > 2**32 * h_len:
        raise ValueError("Máscara muito longa para aplicar mgf")
     
    t=b""

    for i in range(math.ceil(len/h_len)):
        c = i.to_bytes(4, byteorder="big")
        t += hashlib.sha256(seed+c).digest()

    return  t[:len]

def oaep_encode(msg, enLen=128, seed=None):

    hLen = hashlib.sha256().digest_size
    mLen = len(msg)

    psLen = enLen - mLen -2*hLen-1

    if(mLen>psLen):
        raise ValueError("Mensagem muito longa para ser encriptada por OAEP")
    
    PS = b"\x00" * psLen

    DB = PS+b"\x01" +msg
    print(DB)
    
    if seed is None:
        seed = os.urandom(hLen)
    dbMask = mgf(seed, enLen-hLen)
    maskedDB = bytes(x ^ y for x, y in zip(DB, dbMask))
    
    seedMask = mgf(maskedDB, hLen)
    maskedSeed = bytes(x ^ y for x, y in zip(seed, seedMask))
    
    EM = maskedSeed + maskedDB
    
    return EM


# p = gen_prime()
# q = gen_prime()
# fi_n= (p-1)*(q-1)
# d = gen_d(fi_n)
# e= mod_inv(d,fi_n)


def oaep_decode(EM,enLen =128):
    hLen = hashlib.sha256().digest_size
    if(enLen<hLen+1):
        raise ValueError("Mensagem muito curta para ser decriptada por OAEP")

    maskedSeed = EM[:hLen]
    maskedDB = EM[hLen:]

    seedMask = mgf(maskedDB,hLen)
    
    seed = bytes(x ^ y for x, y in zip(maskedSeed, seedMask))

    dbMask = mgf(seed,enLen-hLen)
    DB = bytes(x ^ y for x, y in zip(maskedSeed, dbMask))


    print("******:",DB)

    M = DB[hLen:].split(b'\x01', 1) 
    return M

EM = b"\x04"  


# message = oape_encode(EM)
# print(oaep_decode(message))



# Recodar a decode
# Ver se eu mecho para bytes
#   psLen = enLen - mLen -2*hLen-1 -> VER SE TODOS ESSES VALORES ESTÃO EM BUYTES
# Sera que eu preciso dividir a msg a ser encriptada?
# Talvez tirar o enLen (?)
#Formula for emLen:
# The length of the encoded message emLen (or oLen) is determined by the size of the RSA modulus (n), as the encoded message will be used as an input to the RSA encryption algorithm.

# The length of emLen is defined as:

# emLen = (n.bit_length() + 7) // 8

# 