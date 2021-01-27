from .chiffrement import *
from ressources.tools import *
import ressources.RC4 as RC4

def kasumi_decrypt_ECB(encrypted_content, master_key):
	#initialisation 
	Sbox1, Sbox2 = RC4.get_Sbox_from_key(master_key)
	sub_blocs_en , offset = encrypted_content
	KL, KO, KI = prep_keys(master_key) #les sous clés sont en 16 bits
	clear_text = 0

	#*------------------------*
	#Première boucle pour parcourir les "blocs" de données de 64 bits
	for sub_bloc in sub_blocs_en: 
		#left et right sont des entier de 32 bits
		left, right = split(sub_bloc, splitPos=32, blockSize=64) 
		#Deuxième boucle contenant l'algorithme kasumi
		for iteration in range(7,-1, -1): #produit une suite [7, 6, 5, 4, 3, 2, 1, 0]
			right, left = left , right
			right = mainFunction(iteration, left, KO[iteration], KI[iteration] , KL[iteration] , Sbox1, Sbox2) ^ right
		decrypted_bloc = merge(left, right, rightNbOfBits=32)

		#Concaténation en tenant compte du offset
		if sub_bloc == sub_blocs_en[-1]:
			clear_text = (merge(clear_text, decrypted_bloc, rightNbOfBits=(offset[-1]+len(bin(decrypted_bloc)[2:]))))
		else :
			clear_text = (merge(clear_text, decrypted_bloc, rightNbOfBits=64))
	return text_from_bits(bin(clear_text)[2:])

def kasumi_decrypt_CBC(encrypted_content, master_key):
	#initialisation 
	Sbox1, Sbox2 = RC4.get_Sbox_from_key(master_key)
	sub_blocs_en , offset = encrypted_content	
	KL, KO, KI = prep_keys(master_key)
	#Les valeurs du vecteur initial sont prises de manière arbitraire
	vecteur_initial = merge(merge(KL[3][0], KL[1][1], rightNbOfBits=16), merge(KL[6][1], KL[0][1], rightNbOfBits=16), rightNbOfBits=32) 
	#Lors de l'itération à travers sub_bloc_en, on ne souhaite pas modifier les sub_blocs pour y refaire référence par la suite
	#on en créé une sauvegarde
	sub_blocs_en_copy = sub_blocs_en.copy()
	clear_text = 0

	#*------------------------*
	for sub_bloc in sub_blocs_en:
		left, right = split(sub_bloc, splitPos=32, blockSize=64) 
		for iteration in range(7,-1, -1):
			right, left = left , right
			right = mainFunction(iteration, left, KO[iteration], KI[iteration] , KL[iteration] , Sbox1, Sbox2) ^ right 
		decrypted_bloc = merge(left, right, rightNbOfBits=32)
		
		# XOR propre au CBC
		if sub_bloc == sub_blocs_en[0]:
			decrypted_bloc = decrypted_bloc ^ vecteur_initial
		else : 
			decrypted_bloc = decrypted_bloc ^ sub_blocs_en_copy[0]
			sub_blocs_en_copy.pop(0) #Le premier element de la liste dupliquée est supprimé de sorte que sub_blocs_en_copy[0]
			#fasse tout le temps référence à l'avant dernier bloc chiffré

		#Concaténation en tenant compte du offset
		if sub_bloc == sub_blocs_en[-1]:
			clear_text = (merge(clear_text, decrypted_bloc, rightNbOfBits=(offset[-1]+len(bin(decrypted_bloc)[2:]))))
		else :
			clear_text = (merge(clear_text, decrypted_bloc, rightNbOfBits=64))
	return text_from_bits(bin(clear_text)[2:])


def kasumi_decrypt_PCBC(encrypted_content, master_key):
	#initialisation 
	Sbox1, Sbox2 = RC4.get_Sbox_from_key(master_key)
	sub_blocs_en , offset = encrypted_content	
	KL, KO, KI = prep_keys(master_key) 
	clear_text = 0
	vecteur_initial = merge(merge(KL[3][0], KL[1][1], rightNbOfBits=16), merge(KL[6][1], KL[0][1], rightNbOfBits=16), rightNbOfBits=32) 
	sub_blocs_en_copy = sub_blocs_en.copy()

	#*------------------------*
	for sub_bloc in sub_blocs_en: 
		left, right = split(sub_bloc, splitPos=32, blockSize=64) 
		for iteration in range(7,-1, -1): 
			right, left = left , right
			right = mainFunction(iteration, left, KO[iteration], KI[iteration] , KL[iteration] , Sbox1, Sbox2) ^ right 
		decrypted_bloc = merge(left, right, rightNbOfBits=32)
		
		#XOR propre au PCBC
		if sub_bloc == sub_blocs_en[0]:
			decrypted_bloc = decrypted_bloc ^ vecteur_initial
		else : 
			decrypted_bloc = decrypted_bloc ^ sub_blocs_en_copy[0] ^ bloc_retenu
			sub_blocs_en_copy.pop(0) 
		bloc_retenu = decrypted_bloc

		#Concaténation en tenant compte du offset
		if sub_bloc == sub_blocs_en[-1]:
			clear_text = (merge(clear_text, decrypted_bloc, rightNbOfBits=(offset[-1]+len(bin(decrypted_bloc)[2:]))))
		else :
			clear_text = (merge(clear_text, decrypted_bloc, rightNbOfBits=64))
	return text_from_bits(bin(clear_text)[2:])



