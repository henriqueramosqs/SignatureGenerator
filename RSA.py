import random

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
    
    

def is_composite(n:int, a:int, d:int, s:int)->bool:
    res = Mod(a,n)**d
    if(res==1 or res == n-1):
        return False
    
    for _ in range(1,s):
        res*=2
        if(res==n-1):
            return False
        
    return True

def is_prime(n:int, iter:int)->bool:

    if(n < 4):
        return n == 2 or n == 3

    s = 0
    d = n - 1

    while((d & 1) == 0):
        d >>= 1
        s+=1
    
    for _ in range(iter):
        a = 2+ random.randint()%(n-3)
        if(is_composite(n,a,d,s)):
            return False
        
    return True

def gen_prime(bits:int):
    ans=random.getrandbits(bits)
    while(not is_prime(ans)):
        continue
    return ans


