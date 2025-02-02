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
        if ((1<<(bits-1))<n) and is_prime(n):
            return n

def gen_d(fi_n:int):
    while True:
        d = random.randint(1,fi_n)
        if math.gcd(d,fi_n)==1:
            return d

def rsa_encrypt(msg, e, n):
    m = int.from_bytes(msg, 'big')
    c = pow(m, e, n)
    return c.to_bytes((n.bit_length() + 7) // 8, 'big')

def rsa_decrypt(cipher, d, n):
    c = int.from_bytes(cipher, 'big')
    m = pow(c, d, n)
    return m.to_bytes((n.bit_length() + 7) // 8, 'big')

EM = b"\x04" 

def mgf(seed: bytes, mask_len: int):
    h_len = hashlib.sha256().digest_size
    if mask_len > (2 ** 32) * h_len:
        raise ValueError("mask_len grande demais")

    mask = b''
    for i in range(math.ceil(mask_len / h_len)):
        c = i.to_bytes(4, byteorder="big")
        mask += hashlib.sha256(seed + c).digest()

    return mask[:mask_len]

def oaep_encode(message: bytes, k: int,label: bytes = b"", seed=None) -> bytes:
    h_len = hashlib.sha256().digest_size
    m_len = len(message)

    if m_len > k - 2 * h_len - 2:
        raise ValueError("Mensagem muito longa")
    
    l_hash = hashlib.sha256(label).digest()

    ps_len = k - m_len - 2 * h_len - 2
    ps = b"\x00" * ps_len

    db = l_hash + ps + b"\x01" + message

    if seed is None:
        seed = os.urandom(h_len)
    db_mask = mgf(seed, k - h_len - 1)
    masked_db = bytes(x ^ y for x, y in zip(db, db_mask))

    seed_mask = mgf(masked_db, h_len)
    masked_seed = bytes(x ^ y for x, y in zip(seed, seed_mask))

    em = b"\x00" + masked_seed + masked_db

    return em

def oaep_decode(em: bytes, k: int, label: bytes = b"") -> bytes:
    h_len = hashlib.sha256().digest_size

    if len(em) != k or k < 2 * h_len + 2:
        raise ValueError("Erro de decriptação: Tamanho da mensagem incompatível")

    masked_seed = em[1:h_len + 1]
    masked_db = em[h_len + 1:]

    l_hash = hashlib.sha256(label).digest()

    seed_mask = mgf(masked_db, h_len)
    seed = bytes(x ^ y for x, y in zip(masked_seed, seed_mask))

    db_mask = mgf(seed, k - h_len - 1)
    db = bytes(x ^ y for x, y in zip(masked_db, db_mask))

    l_hash_prime = db[:h_len]
    if l_hash_prime != l_hash:
        raise ValueError("Mismatch entre os hashs das labels")

    try:
        ps, message = db[h_len:].split(b"\x01", 1)
    except ValueError:
        raise ValueError("Erro de decriptação: padding iválido")

    return message