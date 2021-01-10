"""
interface utilisateur
"""
from chiffrement import *
from dechiffrement import *
from gen_cle import gen_premier, trouve_Zn, publickey, privatekey
from SHA_1 import SHA_1
from fonction_eponge import eponge
import Signature_ElGamal
import RSA
import pickle
import blockchain
from pip._vendor.pyparsing import originalTextFor


prime, alpha = 9897945769718193639959984638000900286314127960826347487029072470408703069670883110279720785601634769147223130343953316018693873378437092702305231198650081, 7867969773067674666283917880578211989084312205422864583887419974689917662993740993709666012206421341523769293969182149676889796906645634003337407639637527


PROMPT = ">>> "

def main_menu_sequence():
	print("CHARGEMENT ...")
	print("-----------------*")

	while True:
		MENU_SEQUENCE = "Bonjour ô maître Rémi ! Que souhaitez vous faire aujourd’hui ?\n ->1<- Chiffrer un message.\n ->2<- Déchiffrer un message.\n ->3<- Générer des couples de clés publiques / privées.\n ->4<- Générer un hash / générer et vérifier une empreinte.\n ->5<- Enter dans le menu de gestion de la blockchain"
		print(MENU_SEQUENCE)
		arg = input(PROMPT)
		if arg == '1': 
			kasumi_encrypt_menu()
		elif arg == '2':
			kasumi_decrypt_menu()
		elif arg == '3':
			gen_couple_cles_menu(prime, alpha)
		elif arg == '4':
			print("Voulez vous générer : \n->1<- Un hash \n->2<- Une empreinte") 
			arg = input(PROMPT)

			if arg == '1':
				hash_menu()
			elif arg == '2':
				signature(prime, alpha)

		elif arg == '5':
			blockchain.main(prime, alpha)
		# elif arg == '6':
		# 	pass
		# elif arg == '7':
		# 	pass
		# elif arg == '8':
		# 	pass
		# elif arg == '9':
		# 	pass

def kasumi_encrypt_menu():
	print("Entrez ici votre clé de chiffrement (ATTENTION, ELLE DOIT ETRE AU MINIMUM DE 16 CARACTERES:") 
	key = input(PROMPT)

	# KASUMI ENCRYPT
	print("Voulez vous \n->1<- écrire le texte à chiffrer ici \n->2<- Chiffrer le texte dans le fichier \"texte_a_chiffrer\"")
	arg = input(PROMPT)

	if arg == '1':
		print("Quel texte voulez vous chiffrer :")
		content = input(PROMPT)
	elif arg == '2':
		f=open("texte_a_chiffrer.txt", "r")
		if f.mode == 'r':
			content =f.read()
			print("Le texte à chiffrer est :\n", content)
	
	print('Choisissez un type d\'algorithme. \n->1<- ECB \n->2<- CBC \n->3<- PCBC')
	arg = input(PROMPT)
	if arg == '1':
		encrypted_content = kasumi_encrypt_ECB(content, key)
	elif arg == '2':
		encrypted_content = kasumi_encrypt_CBC(content, key)
	elif arg == '3':
		encrypted_content = kasumi_encrypt_PCBC(content, key)

	print("Resultat du chiffrement : ", encrypted_content)

	with open('texte_chiffré.txt', 'wb') as f:
		pickle.dump(encrypted_content, f)

	print("Votre chiffré se retrouve dans le fichier \"texte_chiffré\"")

def kasumi_decrypt_menu():
	print("Entrez ici votre clé de déchiffrement :") 
	key = input(PROMPT)

	print("ATTENTION, le texte à déchiffrer DOIT se trouver dans le fichier \"texte_chiffré.txt\"")
	
	with open("texte_chiffré.txt", "rb") as f:
		encrypted_content = pickle.load(f)

	print("Le texte à déchiffrer est :\n", encrypted_content)
	
	print('Choisissez un type d\'algorithme. \n->1<- ECB \n->2<- CBC \n->3<- PCBC')
	arg = input(PROMPT)
	if arg == '1':
		decrypted_content = kasumi_decrypt_ECB(encrypted_content, key)
	elif arg == '2':
		decrypted_content = kasumi_decrypt_CBC(encrypted_content, key)
	elif arg == '3':
		decrypted_content = kasumi_decrypt_PCBC(encrypted_content, key)
	
	print("Resultat du déchiffrement : ", decrypted_content)

def gen_prime_et_alpha():
	prime=gen_premier()
	print("Le nombre n suivant est PREMIER :", prime)
	print("")

	#Trouver élément générateur de Zprime
	alpha=trouve_Zn(prime)
	print("Un élement générateur de Zn :", alpha)
	print("")
	return prime, alpha

def gen_couple_cles_menu(prime, alpha):

	#Génération d'un couple de clés pour Alice et Bob
	clés_alice = publickey(prime, alpha)
	AlicePublicKey = clés_alice[0]
	AliceSecret = clés_alice[1]
	AlicePrivateKey = privatekey(AlicePublicKey, prime, AliceSecret)

	print( "GENERATION DE CLE\n-------------------------*\nCLE PUBLIC : \n", AlicePublicKey,"\n-------------------------*\nCLE PRIVEE : \n", AlicePrivateKey)
	print("\n\nCes clés ont été sauvegardées dans \"generated_public_key\" et \"generated_private_key\"\n")
	with open('generated_public_key.txt','wb') as fichier:
		mon_pickler=pickle.Pickler(fichier)
		mon_pickler.dump(AlicePublicKey)
	
	#stockage secrets
	with open('generated_private_key.txt','wb') as fichier2:
		pickler=pickle.Pickler(fichier2)
		pickler.dump(AliceSecret)
	return AlicePublicKey , AlicePrivateKey, AliceSecret

def hash_menu():
	print("Voulez vous utiliser la fonction éponge ? \n->1<- Non \n->2<- Oui")
	arg = input(PROMPT)
	print("Entrez ici le texte à hasher") 
	texte = input(PROMPT)

	if arg == '1': 
		print("Resultat du hash :\n", SHA_1(texte),"\n")
	elif arg == '2':
		print("Resultat du hash :\n",eponge(texte),"\n")

def signature(prime, alpha):
	print("Entrez le texte à signer") 
	texte = input(PROMPT)
	print("Quel type de signature ? \n->1<- El-Gamal \n->2<- RSA") 
	arg = input(PROMPT)
	
	if arg == '1': 
		print("Qui est à l'origine du message ? \n->1<- Alice \n->2<- Bob")
		source = int(input(PROMPT))
		texte_hashé = SHA_1(texte)
		verif = False
		origin = "none"
		s1 = 0
		s2 = 0
		AlicePublicKey , AlicePrivateKey, AliceSecret = gen_couple_cles_menu(prime, alpha)
		BobPublicKey , BobPrivateKey, BobSecret = gen_couple_cles_menu(prime, alpha)
		if source == 1 :
			s1, s2 = Signature_ElGamal.sign(texte_hashé, alpha, prime, AliceSecret)
		elif source == 2 :
			s1, s2 = Signature_ElGamal.sign(texte_hashé, alpha, prime, BobSecret)
		print("La signature est la suivante :", s1, s2)	
		print("Vérifier qu'Alice ou Bob est bien à la source du message ? \n->1<- Alice \n->2<- Bob")
		arg = input(PROMPT)
		if arg == '1': 
			verif = Signature_ElGamal.verif(SHA_1(texte), alpha, prime, s1, s2 , AlicePublicKey)
			origin = "Alice"
		elif arg == '2':
			verif = Signature_ElGamal.verif(SHA_1(texte), alpha, prime, s1, s2 , BobPublicKey)
			origin = "Bob"
		if verif == True:
			print("L'empreinte du message et l'empreinte issue du déchiffrement de la signature sont identiques")
			print("Le message est intègre et " + origin + " en est bien l'auteur\n")
		else:
			print("L'intégrite et l'authentification du message n'ont pas pu être vérifiés\n")


	# ECHANGE RSA
	elif arg == '2':


		print("Deux nombres copremiers ont déjà été stockés pour aller plus vite")
		AlicePublicKey , AlicePrivateKey = RSA.init_alice(13332144011952475692844792665277339251038471684167210337080000835564590838277715004334349821463460988563502376804559805790138591307572695202210152239440283, 6666072005976237846422396332638669625519235842083605168540000417782295419138857502167174910731730494281751188402279902895069295653786347601105076119720141)
		BobPublicKey, BobPrivateKey = RSA.init_alice(1577467455571380271454607668688925369906512098969436445939189470935532055802488990968232233070389803383199415953060598110246971828956721293333253157891483, 788733727785690135727303834344462684953256049484718222969594735467766027901244495484116116535194901691599707976530299055123485914478360646666626578945741)
		
		print("Qui est à l'origine du message ? \n->1<- Alice \n->2<- Bob")
		arg = input(PROMPT)

		if arg == '1':
			print("Génération d'un couple de clés \n PUBLIC_KEY:", AlicePublicKey, '\nPRIVATE_KEY', AlicePrivateKey)
			print("Signature RSA par la clé privée d'Alice")
			signature = RSA.text_signature(texte, AlicePrivateKey)
		if arg == '2':
			print("Génération d'un couple de clés \n PUBLIC_KEY:", BobPublicKey, '\nPRIVATE_KEY', BobPrivateKey)
			print("Signature RSA par la clé privée de Bob")
			signature = RSA.text_signature(texte, BobPrivateKey)		
		
		print("RESULTAT DE LA SIGNATURE PAR RSA AVEC UNE CLE PRIVEE: \n", signature)
		print("Vérificiation de la signature. Vérifier qu'Alice ou Bob est bien à la source du message ? \n->1<- Alice \n->2<- Bob")
		arg = input(PROMPT)
		if arg == '1': 
			result = RSA.bob_signature_verification(unchecked_message=texte, signature=signature, public_key=AlicePublicKey)
			origin = "Alice"
		elif arg == '2':
			result = RSA.bob_signature_verification(unchecked_message=texte, signature=signature, public_key=BobPublicKey)
			origin = "Bob"

		if result:
			print("L'empreinte du message et l'empreinte issue du déchiffrement de la signature sont identiques")
			print("Le message est intègre et " + origin + " en est bien l'auteur\n")
		else:
			print("L'intégrite et l'authentification du message n'ont pas pu être vérifiés\n")



main_menu_sequence()
