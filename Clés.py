'''
Created on 17 nov. 2020

@author: Test
'''
import random  
  
#------------------------------------------------Part 1 : Générer un entier premier n de 512 bits
  
#Exponentiation modulaire
#Renvoie (x^y) % p 
def power(x, y, p): 
    res = 1;  
    x = x % p;  
    while (y > 0): 
        if (y & 1): 
            res = (res * x) % p; 
        y = y>>1;
        x = (x * x) % p; 
      
    return res; 
  
  
def MiillerRabinTest(d, n): 
    a = 2 + random.randint(1, n - 4); 
  
    x = power(a, d, n); 
  
    if (x == 1 or x == n - 1): 
        return True; 
    while (d != n - 1): 
        x = (x * x) % n; 
        d *= 2; 
        if (x == 1): 
            return False; 
        if (x == n - 1): 
            return True; 
    return False; 
  
#Renvoie vrai si n probalement premier (avec k précision) et faux si n n'est pas premier
def isPrime( n, k): 
    if (n <= 1 or n == 4): 
        return False; 
    if (n <= 3): 
        return True; 
    d = n - 1; 
    while (d % 2 == 0): 
        d //= 2; 
    for i in range(k): 
        if (MiillerRabinTest(d, n) == False): 
            return False;   
    return True; 

#------------------------------------------------Part 2 : Trouver un élement générateur de Zn  

#Décomposition en facteurs premiers
def decompose(num,s): 
    print("n - 1 : %d = 1"%(num), end=' ')
    i=2 
    while num>1: 
        while num%i==0: 
            print("x",i, end=' ') 
            num=num/i 
            s.add(i)
        i=i+1
    print("")
    print("")

#--------------------------------------------------------------------------
#Il faut prouver que g^k (avec k=((p-1)/q) avec q facteur premier de p-1) différent de 1 mod p pour tous ses facteurs premiers.
#Si oui, alors g est générateur. Sinon on test avec g+1 (g premier)


def generateur(g):
    print("Test pour g =", g)
    print("")
    i=len(t)-1
    b = t[i]
    j = 1
    condition=0
    print("facteur = ", b)
    print("calcul ",j, "/", len(t), "=",(g**(num/b))%n)
    while (g**(num/b))%n != 1:
        i = i - 1
        j = j + 1
        b = t[i]
        print("facteur = ", b)
        print("calcul ",j, "/", len(t), "=",(g**(num/b))%n)
        if j == len(t):
            condition=1 
            break;           
    if condition==1:
        print(g," est un générateur du groupe Zn")
        return True;
    else:
        print(g, "n'est pas un générateur")
        return False;
    print("-----------------------")


#--------------------------------------main()   
n = random.getrandbits(10)
while not isPrime(n,30):
    n = random.getrandbits(10)
print("Ce nombre n est PREMIER :", n)

s = set()
num=n-1    
decompose(num,s) 
q = list(s)
t = sorted(q)
print("Nombres de facteurs premiers distincts :", len(t))
print("Facteurs premiers :", t)
    
g=3
print("")
while not generateur(g):
    g=g+1
    while not isPrime(g, 10):
        g=g+1
        
    

