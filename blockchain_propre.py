import SHA_1
from datetime import datetime
import random
from Clés import *
from Signature_ElGamal import *
import Signature_ElGamal
from pickle import FALSE

#Rajouter une fonction pour récompenser les mineurs ?
#Implémenter la fonction new bloc dans mine (plus logique)


#Calcul du hash du bloc entier (index + previoushash + timestamp + salt + transactions)
def calculateHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.salt) + str(block.confirmedtransactions)
    return (SHA_1.SHA_1(bloc))


#Classe d'un Block
class Block(object):
    def __init__(self, index, previousHash, timestamp, transactions):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.salt = 0
        self.confirmedtransactions = transactions
        self.hash = calculateHash(self)    
    
    #Fonction de minage d'un block  
    def mineBlock(self, difficulty):
        s1 = str(self.hash)
        zeros = str("0"*difficulty)
        self.salt = 0
        while not s1.endswith(zeros):
            #self.salt = self.salt + 1
            self.salt = random.getrandbits(100)
            self.hash = calculateHash(self)
            s1 = str(self.hash)
            

#Classe de la Blockchain
class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = []
        self.pending_transactions = []
        
        #Génération du premier block de la chaîne
        genesisBlock = Block(0, None, datetime.now(), self.pending_transactions)#laisser None ?
        genesisBlock.mineBlock(self.difficulty)
        self.chain.append(genesisBlock)
        
    #Renvoie le block précédent
    @property
    def last_block(self):
        return self.chain[-1]
    
    #Création d'un nouveau block    
    def newBlock(self):    
        latestBlock = self.chain[-1]
        #Réinitialisation de la liste des transactions en attente quand création d'un nouveau block
        self.pending_transactions = []
        return(Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), self.pending_transactions))
    
#----------------------------------#ajout bloc : ajout transactions (vérifier signature transaction avant son ajout) : minage du bloc : création nouveau bloc : ...

    #Minage puis vérification du block avant l'ajout à la chaîne
    def addBlock(self, block):
        block.mineBlock(self.difficulty)
        if self.isValidBlock(block, self.last_block):
            self.chain.append(block)
        else:
            print("block non valide pour être ajouté à la chaîne")
            
    def verify_transaction_signature(self, sender_secret, sender_pk, transaction):
        h = SHA_1.SHA_1(str(transaction))
        signature = sign(h, alpha, prime, sender_secret)
        s1 = signature[0]
        s2 = signature[1]
        if not verif(h, alpha, prime, s1, s2, sender_pk):
            print("Fail vérif signature")
            return False
        return True
    
    #Création d'une transaction
    def new_transaction(self, source, destination, amount, sender_secret, sender_pk):
        transaction = {
            'sender': source,
            'receiver' : destination,
            'amount' : amount,
            }
        if self.verify_transaction_signature(sender_secret, sender_pk, transaction):
            self.pending_transactions.append(transaction)
        else:
            print("Echec de l'ajout de la transaction")
    

    
#---------------------------------------- Vérification de la blockchain
    
    #Vérification validité du premier bloc             
    def isFirstBlockValid(self):
        firstBlock = self.chain[0]
        
        #Vérification de l'index
        if firstBlock.index != 0:
            print("Erreur : index du premier bloc incorrect")
            return False
        
        #Vérification du previous_hash
        if firstBlock.previousHash is not None:
            print("Erreur : 'previous_hash' du premier bloc incorrect - Should be 'None'")
            return False
        
        #Vérification du hash
        if (firstBlock.hash is None or calculateHash(firstBlock) != firstBlock.hash):
            print("Erreur : hash du premier bloc incorrect")         
            return False
        return True
    
    
    #Vérification validité d'un bloc                
    def isValidBlock(self, block, previousBlock):
        ind = block.index
        
        #Vérification de l'index
        if previousBlock.index+1 != block.index:
            print("Erreur : index du bloc " +str(ind)+ " incorrect")
            return False
        
        #Vérification du previous_hash
        if (block.previousHash is None or block.previousHash != previousBlock.hash):
            print("Erreur : hash du bloc " + str(ind-1) +" différent du hash du bloc "+str(ind))
            return False
        
        #Vérification du hash
        if (block.hash is None or calculateHash(block) != block.hash):
            print("Erreur : hash du bloc " + str(ind) +" différent du hash calculé")
            return False
        
        #Vérification de la preuve de calcul : recalculer le hash et voir s'il correspond à la difficulté définie pour le minage
        if not (str(calculateHash(block)).endswith(str("0"*self.difficulty))):
            print("Erreur : preuve non valide pour le block " + str(ind))
            return False      
            
        return True   
    
    #Vérification de la chaîne entière
    def isBlockchainValid(self):
        
        #Vérification premier bloc
        if not self.isFirstBlockValid():
            print("error1")
            return False
        else:
            print("Vérification du premier bloc réussie !")
                
        #Vérification des blocs suivants
        m=0
        for i in range(1, len(self.chain)):
            previousBlock = self.chain[i-1]
            block = self.chain[i]
            if not self.isValidBlock(block, previousBlock):
                m+=1
                return False 
        if m == 0:
            print("Vérification des blocs suivants réussie !")                     
        return True


#---------------------------------------- Affichage
        
    #Affichage de la blockchain
    def display(self):
        j=1
        print("")
        for block in self.chain:           
            chain = "Block #"+str(block.index)+" ["+"\n\tindex: "+str(block.index)+"\n\tprevious hash: "+str(block.previousHash)+"\n\ttimestamp: "+str(block.timestamp)
            print(str(chain))
            if block.index == 0:
                trans = ("\tTransaction : None")
                print(trans)
            else:
                for i in range(len(block.confirmedtransactions)):            
                    trans = ("\tTransaction " + str(j) + ": " + (str(block.confirmedtransactions[i]))+" --- Signature vérifiée")
                    print(trans)
                    j+=1               
            chain2 = "\thash: "+str(block.hash)+"\n\tsalt: "+str(block.salt)+"\n]\n"
            print(str(chain2))
            
            
#----------------------------------------
#---------------------------------------- Main() minage : ajout bloc : création nouveau bloc : 

#Générer un nombre premier 'prime' de 512 bits
prime = gen_premier()
    
#Trouver élement générateur 'alpha' de Zprime
alpha=trouve_Zn(prime)
    
#Génération de la clé publique et du secret d'Alice
Alice = publickey(prime, alpha)
pk_Alice=Alice[0]
secret_Alice=Alice[1]
Bob = publickey(prime, alpha)
pk_Bob=Bob[0]
secret_Bob=Bob[1]

blockchain = Blockchain(2)
b1 = blockchain.newBlock()
t1 = blockchain.new_transaction("Pierre", "Benoit", "135 BTC", secret_Alice, pk_Alice)#faire correspondre source et clés 
t2 = blockchain.new_transaction("Rémi", "Pascal", "Pain", secret_Bob, pk_Bob)
blockchain.addBlock(b1)

b2 = blockchain.newBlock()
t3 = blockchain.new_transaction("Hivette", "René", "Lait", secret_Alice, pk_Alice)
t4 = blockchain.new_transaction("JPP", "Clair", "Chazal", secret_Bob, pk_Bob)
blockchain.addBlock(b2)

print("Validité de la blockchain :", blockchain.isBlockchainValid())
blockchain.display()
