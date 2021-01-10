
import random  
from random import randint, shuffle, choice
import pickle

#------------------------------------------
#------------------------------------------ Part 1 : Fonctions pour vérifier qu'un large entier n est premier
#------------------------------------------
  
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
  
#Fonction test de primalité de Miller-Rabbin 
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


#------------------------------------------ 
#------------------------------------------ Part 2 : Fonctions pour trouver un élement générateur de Zn  
#------------------------------------------ 


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


#Trouver un élément générateur alpha
def gen_alpha(comb, prime_number):
    alpha=randint(0,prime_number - 1)
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


#------------------------------------------ 
#------------------------------------------ Part 3 : Fonctions pour la génération d'un couple de clés publique/privée
#------------------------------------------ 

#Génération d'un nombre premier 'prime' de 512 bits 
def gen_premier():
    #Génrérer un nombre de 512 bits aléatoirement
    prime = random.getrandbits(512)
    #Application du test de Miller-Rabin pour vérifier la primalité du nombre généré
    while not isPrime(prime,10):
        prime = random.getrandbits(512)
    return prime

#Trouver un élément générateur de Zprime
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

#-------------- Générer un couple de clés publiques/privées --------------#

#génération clés publiques
def publickey(prime,alpha):
    secret = randint(int(prime/2), int(prime-1))
    #secret = randint(2, 150)-----------------------changer ?
    public_key = power(alpha, secret, prime)
    return (public_key, secret)

#génération clé partagée
def privatekey(public_key_ext, prime, secret):
    private_key = power(public_key_ext, secret, prime)
    return private_key

        
#---------------------------------------------------------------
#---------------------------------------------------------------    main()
#---------------------------------------------------------------

# #Génération premier prime de 512 bits
# prime=gen_premier()
# print("Le nombre n suivant est PREMIER :", prime)
# print("")

# #Trouver élément générateur de Zprime
# alpha=trouve_Zn(prime)
# print("Un élement générateur de Zn :", alpha)
# print("")

#Génération d'un couple de clés pour Alice et Bob
# clés_alice = publickey(prime, alpha)
# AlicePublicKey = clés_alice[0]
# AliceSecret = clés_alice[1]

# clés_bob = publickey(prime, alpha)
# BobPublicKey = clés_bob[0]
# BobSecret = clés_bob[1]

# clés_remi = publickey(prime, alpha)
# RemiPublicKey = clés_remi[0]
# RemiSecret = clés_remi[1]

# #Vérification calcul clé partagée
# AlicePrivateKey = privatekey(BobPublicKey, prime, AliceSecret)
# BobPrivateKey = privatekey(AlicePublicKey, prime, BobSecret)
# if AlicePrivateKey == BobPrivateKey:
#     print("Clé secrète partagée :", AlicePrivateKey)
    
# #------------------------------------------    
# #------------------------------------------ Part 4 : Stockage et lecture dans fichier
# #------------------------------------------

#     #stockage clés publiques
# with open('publickeys.txt','wb') as fichier:
#     mon_pickler=pickle.Pickler(fichier)
#     mon_pickler.dump(AlicePublicKey)
#     mon_pickler.dump(BobPublicKey)
#     mon_pickler.dump(RemiPublicKey)
    
#     #stockage secrets
# with open('privatekey.txt','wb') as fichier2:
#     pickler=pickle.Pickler(fichier2)
#     pickler.dump(AliceSecret)
#     pickler.dump(BobSecret)
#     pickler.dump(RemiSecret)

   
#     # lecture clés publiques
# with open('publickeys.txt','rb') as fichier:
#     mon_depickler=pickle.Unpickler(fichier)
#     AlicePublicKey=mon_depickler.load()
#     BobPublicKey=mon_depickler.load()
#     RemiPublicKey=mon_depickler.load()

#     #lecture secrets
# with open('privatekey.txt','rb') as fichier2:
#     mine=pickle.Unpickler(fichier2)
#     AliceSecret=mine.load()
#     BobSecret=mine.load()
#     RemiSecret=mine.load()

# print("\nClé publique d'Alice : ", AlicePublicKey)
# print("Secret d'Alice : ", AliceSecret)
# print("")
# print("Clé publique de Bob : ", BobPublicKey)
# print("Secret de Bob : ", BobSecret)
# print("")
# print("Clé publique de Rémi : ", RemiPublicKey)
# print("Secret de Rémi : ", RemiSecret)
# print("")



        