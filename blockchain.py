import SHA_1
from datetime import datetime
import random
from Clés import *
import Clés
import Signature_ElGamal
#from test.test_buffer import verify_structure

prime, alpha = 9897945769718193639959984638000900286314127960826347487029072470408703069670883110279720785601634769147223130343953316018693873378437092702305231198650081, 7867969773067674666283917880578211989084312205422864583887419974689917662993740993709666012206421341523769293969182149676889796906645634003337407639637527


#Classe pour la création des utilisateurs (user : nom, argent, clé secrète, clé publique)
class User(object):
    """personne tenant un portefeuille"""
    def __init__(self, prime, alpha):
        super(User, self).__init__()
        self.nom = input("Entrer votre nom d'utilisateur : ")
        while self.nom.isdigit() or len(self.nom ) < 3 or len(self.nom ) > 15:
            self.nom = input("Veuillez svp entrer un nom d'utilisateur valide : ")        
        self.money = input("Entrer l'argent que vous détenez : ")
        while not (self.money.isdigit() and (int(self.money) > 0)):
            self.money = input("Entrer un montant valide : ")
        self.money = int(self.money)
        clés = publickey(prime, alpha)
        self.public_key = clés[0]
        self.secret = clés[1]    

#Classe d'un Block (block : index, previous_hash, timestamp, salt, count, transactions)
class Block(object):
    def __init__(self, index, previousHash, timestamp, transactions):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.salt = 0
        #count : nombre de tentatives avant le minage du bloc
        self.count=0
        self.confirmedtransactions = transactions
        self.hash = calculateHash(self)    
    
    #Fonction de minage d'un block
    #Difficulty : définit le nombre de bits à 0 à la fin du hash pour le minage du bloc
    def mineBlock(self, difficulty):
        s1 = str(self.hash)
        zeros = str("0"*difficulty)
        self.salt = 0
        self.count = 0
        while not s1.endswith(zeros):
            self.count += 1
            self.salt = random.getrandbits(100)
            self.hash = calculateHash(self)
            s1 = str(self.hash)
            
#Calcul du hash du bloc entier (index + previoushash + timestamp + salt + count + transactions)
def calculateHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.salt) +  str(block.count) + str(block.confirmedtransactions)
    return (SHA_1.SHA_1(bloc))

#Classe de la Blockchain
class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        #chain : liste des blocks de la blockchain
        self.chain = []
        #pending_transactions: transactions en attente
        self.pending_transactions = []
        self.list_users = []
        self.all_transactions = []
        #blocks : liste des blocks avant ajout à la blockchain
        self.blocks = []
        self.sign1 = []
        self.sign2 = []
        
        #Génération du premier block de la chaîne
        genesisBlock = Block(0, None, datetime.now(), None)
        genesisBlock.mineBlock(self.difficulty)
        self.chain.append(genesisBlock)
    
    #Création des utilisateurs    
    def create_users(self, prime, alpha):
        nombre_user = input("Combien d'utilisateur voulez-vous créer ? : ")
        print ("Exemple avec les utilisateurs Benoit et Pierre\n")
        while not (nombre_user.isdigit() and (int(nombre_user) > 0)):
            nombre_user = input("Veuillez entrer un nombre d'utilisateurs correct : ")  
        user_count = int(nombre_user)
        i = 1
        while not user_count == 0 :
            user = User(prime, alpha)
            self.list_users.append(user)
            print("Utilisateur " + str(i) + " / " + str(nombre_user) + " créé.\n")
            user_count -= 1
            i += 1
        self.display_users()
        
#----------------------------------------
#---------------------------------------- Création et ajout des blocks à la blockchain
#---------------------------------------- Création d'un bloc --> ajout des transactions (2 max par block) --> : minage du bloc --> ajout du block à la chaîne : ...   
#----------------------------------------
    
    #Renvoie le block précédent
    @property
    def last_block(self):
        return self.chain[-1]
    
    #Création d'un nouveau block avec les paramètres du block précédent
    def newBlock(self):    
        latestBlock = self.chain[-1]
        new_block = Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), self.pending_transactions)
        self.blocks.append(new_block)
        return new_block

    #Minage puis vérification du block avant l'ajout à la chaîne
    def addBlock(self, block):
        block.mineBlock(self.difficulty)
        if self.isValidBlock(block, self.last_block):
            self.chain.append(block)
            #Réinitialisation de la liste des transactions en attente quand création d'un nouveau block
            self.pending_transactions = []
        else:
            print("block non valide pour être ajouté à la chaîne")


#----------------------------------------
#---------------------------------------- Transactions et signatures des transactions
#----------------------------------------
            
    #Vérification de la signature d'une transaction       
    def verify_transaction_signature(self, source, transaction):
        source_secret = 0
        source_public_key = 0
        for user in self.list_users:
            if user.nom == source:
                source_secret = user.secret
                source_public_key = user.public_key
                break     
        h = SHA_1.SHA_1(str(transaction))
        signature = Signature_ElGamal.sign(h, alpha, prime, source_secret)
        s1 = signature[0]
        s2 = signature[1]
        if s1 not in self.sign1:
            self.sign1.append(s1)
        if s2 not in self.sign2:
            self.sign2.append(s2)
        if not Signature_ElGamal.verif(h, alpha, prime, s1, s2, source_public_key):
            print("Fail vérif signature")
            return False
        return True
    
    #Création d'une transaction avec vérification de sa signature avant sa validation
    # + vérification des paramètres de la transaction (source, destination, amount)
    def new_transaction(self, source, destination, amount):
        amount = int(amount)
        transaction = {
            'sender': source,
            'receiver' : destination,
            'amount (BTC)' : amount,
            } 
        if self.verif_amount(source, destination, amount):
            if self.verify_transaction_signature(source, transaction):
                self.pending_transactions.append(transaction)
                self.all_transactions.append(transaction)
                for user_desti in self.list_users:
                    if user_desti.nom == destination:
                        user_desti.money += amount
                for user_src in self.list_users:
                    if user_src.nom == source:
                        user_src.money -= int(amount)
        else:
            print("Echec de l'ajout de la transaction")
        
    #Vérification du montant de la transaction et du destinataire     
    def verif_amount(self, source, destination, amount):
        receiver_name = 0
        amount = int(amount)
        for user_dest in self.list_users:
            if user_dest.nom == destination:
                receiver_name = user_dest.nom
        for user_source in self.list_users:
            if user_source.nom == source:
                if user_source.money < amount :
                    print("Vous n'avez pas assez d'argent pour effectuer cette transaction")
                    return False
                if user_source.nom == receiver_name :
                    print("Vous ne pouvez pas vous envoyer de l'argent") 
                    return False    
        return True    
    
    #Ajout d'une transaction par un utilisateur 
    def add_transaction(self):
        source = input("Qui envoie de l'argent : ")
        destination = input("A quel destinaire voulez-vous envoyer de l'argent : ")
        amount = input ("Combien voulez-vous envoyer ? : ")
        transaction = {
            'sender': source,
            'receiver' : destination,
            'amount (BTC)' : amount,
            }
        #Max 2 transactions par block
        if self.verify_transaction_signature(source, transaction):
            if len(self.pending_transactions) < 1:
                if self.verif_amount(source, destination, amount):
                    self.new_transaction(source, destination, amount)
                    print("Nouvelle transaction ajoutée avec succès")
            elif len(self.pending_transactions) == 1:
                if self.verif_amount(source, destination, amount):
                    self.new_transaction(source, destination, amount)
                    block = self.newBlock()
                    self.addBlock(block)
                    print("Nouvelle transaction ajoutée avec succès")           
                    print("Minage du bloc réussie")
                    print("Ajout du bloc à la chaîne")
            
            for i in range(len(self.pending_transactions)):            
                trans = ("\n\tTransaction en attente  :" + (str(self.pending_transactions[i]))+" --- Signature vérifiée")
                print(trans)
        else:
            print("Vérification de la signature failed pour la nouvelle transaction")
    
    #Vérification de la signature d'une transaction par un utilisateur        
    def verify_user_transaction(self):
        print(str(len(self.all_transactions)) + " transactions au total")
        index = int(input("Quel transaction voulez-vous vérifier ? : "))
        transaction = self.all_transactions[index-1]
        h = SHA_1.SHA_1(str(transaction))
        print("Transaction " + str(index) + " : " + str(transaction))
        source = input("Qui est à l'origine de la transaction ? : ")
        for user in self.list_users:
            if user.nom == source:
                source_public_key = user.public_key
                break
        s1 = self.sign1[index-1]
        s2 = self.sign2[index-1]   
        if not Signature_ElGamal.verif(h, alpha, prime, s1, s2, source_public_key):
            print("Cette signature n'a pas pu être vérifiée, veuillez contacter Rémi Cogranne")
            return False
        else:
            print("Transaction " + str(index) + " : Signature vérifiée")
            print(source, "est bien à l'origine de cette transaction")
            return True  

#----------------------------------------
#---------------------------------------- Vérification de la blockchain
#----------------------------------------
    
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
            print("hash calculé :", calculateHash(firstBlock))
            print("hash du bloc :", firstBlock.hash)
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
        

#----------------------------------------
#---------------------------------------- Affichage
#---------------------------------------- 
       
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
            chain2 = "\thash: "+str(block.hash)+"\n\tsalt: "+str(block.salt)+"\n\tcount: "+str(block.count)+"\n]\n"
            print(str(chain2)+"\n")
            
        for i in range(len(self.pending_transactions)):            
            trans = ("\tTransactions en attente  :" + (str(self.pending_transactions[i]))+" --- Signature vérifiée")
            print(trans)
            
    #Affichage des utilisateurs
    def display_users(self):
        i = 1
        for user in self.list_users:
            chain = "\tUser " + str(i) + " : " + str(user.nom) + " | Argent disponible : " + str(user.money)
            i += 1
            print(str(chain)+"\n")

    #Affichage du menu
    def menu(self):
        print("\nQue voulez-vous faire ? : ")
        print("\t1 : Ajouter une nouvelle transaction à la chaîne")
        print("\t2 : Vérifier la signature d'une transaction")
        print("\t3 : Vérifier la validité de la blockchain")
        print("\t4 : Afficher les comptes des utilisateurs")
        print("\t5 : Ajouter un utilisateur")
        print("\t6 : Afficher la blockchain")
        print("\t7 : Exit")
        rep = int(input())
        return rep
    
    #Intéractions possibles via le menu
    def play(self):
        turnover=0
        while turnover == 0:
            rep = self.menu()
            if rep == 1:
                self.add_transaction()
            if rep == 2:
                self.verify_user_transaction()
            if rep == 3:
                print("Validité de la blockchain :", self.isBlockchainValid())
            if rep == 4:
                self.display_users()
            if rep ==5:
                self.create_users(prime, alpha)
            if rep == 6:
                self.display()
            if rep == 7:
                print("Fin d'exécution")
                turnover += 1
                
def main(prime, alpha):
    #----------------------------------------------------------------------------------------
    #---------------------------------------- Main() ----------------------------------------
    #----------------------------------------------------------------------------------------

    #Générer un nombre premier 'prime' de 512 bits
    #prime = gen_premier()
        
    #Trouver élement générateur 'alpha' de Zprime
    #alpha = trouve_Zn(prime)

    #Création de la blockchain (10 blocks)
    blockchain = Blockchain(2)
    blockchain.create_users(prime, alpha)

    #Block 1
    b1 = blockchain.newBlock()
    t1 = blockchain.new_transaction("Pierre", "Benoit", "50")
    t2 = blockchain.new_transaction("Benoit", "Pierre", "88")
    blockchain.addBlock(b1)

    #Block 2
    b2 = blockchain.newBlock()
    t3 = blockchain.new_transaction("Benoit", "Pierre", "300")
    t4 = blockchain.new_transaction("Benoit", "Pierre", "4")
    blockchain.addBlock(b2)

    #Block 3
    b3 = blockchain.newBlock()
    t5 = blockchain.new_transaction("Pierre", "Benoit", "127")
    t6 = blockchain.new_transaction("Pierre", "Benoit", "256")
    blockchain.addBlock(b3)

    #Block 4
    b4 = blockchain.newBlock()
    t7 = blockchain.new_transaction("Pierre", "Benoit", "91")
    t8 = blockchain.new_transaction("Benoit", "Pierre", "79")
    blockchain.addBlock(b4)

    #Block 5
    b5 = blockchain.newBlock()
    t9 = blockchain.new_transaction("Pierre", "Benoit", "182")
    t10 = blockchain.new_transaction("Benoit", "Pierre", "232")
    blockchain.addBlock(b5)

    #Block 6
    b6 = blockchain.newBlock()
    t11 = blockchain.new_transaction("Pierre", "Benoit", "225")
    t12 = blockchain.new_transaction("Pierre", "Benoit", "241")
    blockchain.addBlock(b6)

    #Block 7
    b7 = blockchain.newBlock()
    t13 = blockchain.new_transaction("Benoit", "Pierre", "151")
    t14 = blockchain.new_transaction("Pierre", "Benoit", "293")
    blockchain.addBlock(b7)

    #Block 8
    b8 = blockchain.newBlock()
    t15 = blockchain.new_transaction("Benoit", "Pierre", "256")
    t16 = blockchain.new_transaction("Benoit", "Pierre", "130")
    blockchain.addBlock(b8)

    #Block 9
    b9 = blockchain.newBlock()
    t17 = blockchain.new_transaction("Pierre", "Benoit", "280")
    t18 = blockchain.new_transaction("Benoit", "Pierre", "18")
    blockchain.addBlock(b9)

    #Block 10
    b10 = blockchain.newBlock()
    t19 = blockchain.new_transaction("Benoit", "Pierre", "79")
    t20 = blockchain.new_transaction("Pierre", "Benoit", "251")
    blockchain.addBlock(b10)

    #Affichage blockchain et menu
    blockchain.display()
    blockchain.play()

