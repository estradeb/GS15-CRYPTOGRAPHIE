'''
Created on 17 nov. 2020

@author: Test
'''
import random  
from random import randint, shuffle, choice
import pickle
  
#--------------------------------------------------------Part 1 : Fonctions pour la génération d'un entier premier n de 512 bits
  
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

#--------------------------------------------------------Part 2 : Fonctions pour trouver un élement générateur de Zn  

#Décomposition en facteurs premiers
def decompose(prime):
    num = prime - 1
    prime_factors=[]
    #print("n - 1 : %d = 1"%(num), end=' ')
    i=2 
    '''while num>1:'''
    while i * i < num:
        while num%i==0: 
            #print("x",i, end=' ') 
            num=num/i 
            prime_factors.append(i)
        i=i+1
    return prime_factors
    

#Calcul combinatoire des facteurs premiers
def combinaison(prime_factors, n):
    comb = []
    for i in range (len(prime_factors)):
        comb.append(prime_factors[i])
        j = len(prime_factors) - 1
        while j > 1:
            c = prime_factors[i]
            for l in range(i, len(prime_factors), 1):
                c = c * prime_factors[l]
                if c<=(n/2+1):
                    comb.append(c)
                j -= 1
            
    comb=list(set(comb))
    comb.sort()
    return comb

'''#Liste nombres premiers
def list_prime(lower,upper):
    li_prime=[]
    for num in range(lower,upper +1):
        if isPrime(num, 10):
            li_prime.append(num)
    return li_prime   
'''    
           
#Trouver un élément générateur alpha
def gen_alpha(comb, prime_number):
    alpha=randint(0,prime_number-1)
    res = 0
    i = 0
    alpha_group = []
    while i <= ((len(comb)+1)) and alpha < prime_number:
        if res != 1 and i < (len(comb)):
            res = power(alpha, comb[i], prime_number)
            i += 1
        else:
            if res != 1:
                if (len(alpha_group)<3):
                    alpha_group.append(alpha)
                else:
                    shuffle(alpha_group)
                    alpha=choice(alpha_group)
                    break
            alpha += 1
            i=0
            res=0
    return alpha

#--------------------------------------------------------Part 3 : Génération couple de clés publiques et privées

#génération clés publiques
def publickey(prime,alpha):
    secret = randint(int(prime/2), int(prime-1))
    public_key = power(alpha, secret, prime)
    return (public_key, secret)

#génération clé privée
def privatekey(public_key, prime, secret):
    private_key = power(public_key, secret, prime)
    return private_key

#-----Génération nombre premier n de 512 bits 

def gen_premier():
    prime = random.getrandbits(512)
    while not isPrime(prime,10):
        prime = random.getrandbits(512)
    return prime

#-----Trouver un élément générateur de Zn

def trouve_Zn(prime):
    #Décomposition de prime - 1
    prime_factors = decompose(prime)
    #Calcul combinatoire des facteurs premiers 
    comb = combinaison(prime_factors, prime)
    #Génération d'un alpha aléatoire
    alpha = gen_alpha(comb,prime)
    return alpha
    print("Un élement générateur de Zn :", alpha)
    print("")

#-----Générer un couple de clés publiques/privées


def key_gen():
    prime=gen_premier()
    print("Le nombre n suivant est PREMIER :", prime)
    print("")
    alpha=trouve_Zn(prime)
    print("Un élement générateur de Zn :", alpha)
    print("")
    #Génération clé publique pour Alice et Bob
    Alice = publickey(prime, alpha)
    Bob = publickey(prime, alpha)
    
    AlicePublicKey=Alice[0]
    AliceSecret=Alice[1]
    BobPublicKey=Bob[0]
    BobSecret=Bob[1]

    AlicePrivateKey = privatekey(BobPublicKey, prime, AliceSecret)  
    BobPrivateKey = privatekey(AlicePublicKey, prime, BobSecret)  
    
    return AlicePrivateKey, BobPrivateKey, AlicePublicKey, BobPublicKey

#------------------------------- Stockage et lecture dans fichier

def stockage(AlicePrivateKey, BobPrivateKey, AlicePublicKey, BobPublicKey):
    #Clés publiques:
    
    #stockage
    with open('publickeys.txt','wb') as fichier:
        mon_pickler=pickle.Pickler(fichier)
        mon_pickler.dump(AlicePublicKey)
        mon_pickler.dump(BobPublicKey)
    
        #lecture
    with open('publickeys.txt','rb') as fichier:
        mon_depickler=pickle.Unpickler(fichier)
        AlicePublicKey=mon_depickler.load()
        BobPublicKey=mon_depickler.load()

    print("Clé publique d'Alice :", AlicePublicKey)
    print("Clé publique de Bob :", BobPublicKey)
    print("")

    #Clé secrète:

    #stockage
    with open('privatekey.txt','wb') as fichier2:
        pickler=pickle.Pickler(fichier2)
        pickler.dump(AlicePrivateKey)
        pickler.dump(BobPrivateKey)

    #lecture   
    with open('privatekey.txt','rb') as fichier2:
        mine=pickle.Unpickler(fichier2)
        AlicePrivateKey=mine.load()
        BobPrivateKey=mine.load()
    
    #Vérification de des deux clés privées générées
    if AlicePrivateKey == BobPrivateKey:
        print("Clé secrète partagée :", AlicePrivateKey)
        
        
#---------------------------------------------------------------
#---------------------------------------------------------------    main()
#---------------------------------------------------------------

def main_clés():
    clés = key_gen()
    AlicePrivateKey=clés[0]
    BobPrivateKey=clés[1]
    AlicePublicKey=clés[2]
    BobPublicKey=clés[3]
    stockage(AlicePrivateKey, BobPrivateKey, AlicePublicKey, BobPublicKey)
    
main_clés()
    
    
        