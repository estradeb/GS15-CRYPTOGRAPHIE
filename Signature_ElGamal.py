from gen_cle import gen_premier, trouve_Zn, publickey, privatekey, power
from SHA_1 import SHA_1
import random


#------------------------------ Fonctions pour trouver si deux nombres sont premiers entre eux

def pgcd(a,b):
    while b:
        a, b = b, a%b
    return a

def premiers_entre_eux(a,b):
    if( pgcd(a,b) == 1 ):
        return True
    return False

#------------------------------ Signature ElGamal avec la clé privée de l'émetteur

def sign(h, alpha, prime, secret):

    #Choisir un entier k random entre (2,prime-2) avec PGCD(k,(prime-1)) = 1
    k = random.randint(2, prime-2)
    while not premiers_entre_eux(k, prime-1):
        k = random.randint(2, prime-2)

    #S1
    s1=power(alpha, k, prime)

    #S2
    k_1 = pow(k, -1, prime-1)
    s2 = ((h-secret*s1)*k_1) % (prime-1)
     
    #renvoie la signature digitale qui est publique  
    return s1, s2

#------------------------------ Vérification signature ElGamal avec la clé publique de l'émetteur

def verif(h, alpha, prime, s1,s2, pk):

    #empreinte du message avec la même fonction de hashage
    v1 = power(alpha, h, prime)
    
    #empreinte issue du déchiffrement de la signature avec clé publique de l'émetteur
    v2 = (power(pk, s1, prime)*power(s1, s2, prime)) % prime
    
    #Comparaison des deux empreintes
    if 0 < s1 < prime and 0 < s2 < prime-1:
        if v1 == v2:
            return True
        else:
            print("Echec de la vérification de la signature")
            return False
             
#------------------------------
#------------------------------ Initialisation
#------------------------------

'''
#Hash du message
data = "Macron"
print("Message :", data)
h=SHA_1.SHA_1(data)
print("hash =", h)
print("")

#Générer un nombre premier 'prime' de 512 bits
prime = gen_premier()
    
#Trouver élement générateur 'alpha' de Zprime
alpha=trouve_Zn(prime)
    
#Génération de la clé publique et du secret d'Alice
Alice = publickey(prime, alpha)
pk=Alice[0]
secret=Alice[1]

#Signature du message avec le secret d'Alice
s = sign(h, alpha, prime, secret)
s1 = s[0]
s2 = s[1]
print("s1 :", s1)
print("s2 :", s2)

#Vérification de la signature avec la clé publique d'Alice
print("Vérification de la signature :", verif(h, alpha, prime, s1, s2, pk))
'''        

