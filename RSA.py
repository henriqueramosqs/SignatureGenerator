import random
import sys
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
    
    


def is_composite(n: int, a: int, d: int, s: int) -> bool:
    x = Mod(a,n)**d
    
    if x.num == 1 or x.num == n-1:
        return False
    
    for _ in range(s - 1):
        x**=2
        if x.num == n-1:
            return False
    return True

def is_prime(n:int, iter:int=3)->bool:

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
        
p = gen_prime()
q = gen_prime()
print(p,q,sep="\n\n")
