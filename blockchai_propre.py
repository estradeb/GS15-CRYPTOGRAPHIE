from Clés import *
import SHA_1
import random
import string
from datetime import datetime

#Rajouter une fonction pour récompenser les mineurs ?
#Implémenter la fonction new bloc dans mine (plus logique)

def calculateHash(block):#A Mettre dans la classe blockchain ?
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.salt)# + str(block.transactions) 
    return (SHA_1.SHA_1(bloc))


class Block(object):
    def __init__(self, index, previousHash, timestamp, transactions):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.salt = 0
        self.hash = calculateHash(self)
        self.transactions = transactions

      
       
    def mineBlock(self, difficulty):
        s1 = str(self.hash)
        zeros = str("0"*difficulty)
        self.salt = 0
        while not s1.endswith(zeros):
            self.hash = calculateHash(self)
            self.salt = self.salt + 1
            s1 = str(self.hash)


class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chain = []
        self.pending_transactions = []
        
        genesisBlock = Block(0, None, datetime.now(), None)#laisser None ?
        genesisBlock.mineBlock(self.difficulty)
        self.chain.append(genesisBlock)
        
    def newBlock(self):    
        latestBlock = self.chain[-1]
        self.pending_transactions = []
        #Réinitialisation de la liste des transactions en attente quand création d'un nouveau bloc
        return(Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), self.pending_transactions))

    
    
    #Vérification validité du premier bloc             VERBEUSE
    def isFirstBlockValid(self):
        firstBlock = self.chain[0]

        if firstBlock.index != 0:
            return False
        
        if firstBlock.previousHash is not None:
            return False

        if (firstBlock.hash is None or calculateHash(firstBlock) != firstBlock.hash):
            return False

        return True
    
    
    #Vérification validité d'un bloc                VERBEUSE !
    def isValidBlock(self, block):
        previousBlock = self.last_block
        if previousBlock.index+1 != block.index:
            return False

        if (block.previousHash is None or block.previousHash != previousBlock.hash):
            return False
        
        if (block.hash is None or calculateHash(block) != block.hash):
            return False
        if not (str(block.hash).endswith(str("0"*Blockchain.difficulty))):
            return False
            
        return True   
    
    
    def isBlockchainValid(self):
        if not self.isFirstBlockValid():
            return False
        
        for i in range(1, len(self.chain)):
            previousBlock = self.chain[i-1]
            block = self.chain[i]
            if not self.isValidBlock(block, previousBlock):
                return False 

            return True
    

    
    #minage du nouveau bloc pour obtenir un hash valide
    #Faire vérification avant d'ajouter le bloc à la chaîne
    def addBlock(self, block):
        block.mineBlock(self.difficulty)
        self.chain.append(block)
       #if self.isValidBlock(block):
          #self.chain.append(block)
        #else:
            #print("bloc non valide")
        
    def new_transaction(self, source, destination, amount):
        self.pending_transactions.append({
            'source': source,
            'destination' : destination,
            'amount' : amount,
            })
        return self.last_block.index + 1
    
    @property
    def last_block(self):
        return self.chain[-1]
        
    #def add_new_transaction(self, transaction):
        #self.pending_transactions.append(transaction)
    
    def display(self):
        for block in self.chain:
            chain = "Block #"+str(block.index)+" ["+"\n\tindex: "+str(block.index)+"\n\tprevious hash: "+str(block.previousHash)+"\n\ttimestamp: "+str(block.timestamp)+"\n\ttransactions: "+str(block.transactions)+"\n\thash: "+str(block.hash)+"\n\tsalt: "+str(block.salt)+"\n]\n"
            print(str(chain))    

blockchain = Blockchain(2)
b1 = blockchain.newBlock()
t1 = blockchain.new_transaction("Pierre", "Benoit", "135 BTC")
t2 = blockchain.new_transaction("Rémi", "Pascal", "Pain")
blockchain.addBlock(b1)

b2 = blockchain.newBlock()
t3 = blockchain.new_transaction("Hivette", "René", "Lait")
t4 = blockchain.new_transaction("JPP", "Clair", "Chazal")
blockchain.addBlock(b2)

print("Blockchain validity:", blockchain.isBlockchainValid())
blockchain.display()

'''
print("Blockchain ;", blockchain.chain)
print("")
blockchain.display()
'''