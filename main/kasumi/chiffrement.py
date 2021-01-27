
from ressources.tools import *
from main.kasumi.kasumi_tools import *
import ressources.RC4 as RC4

def kasumi_encrypt_ECB(texte, master_key):
	#initialisation 
	Sbox1, Sbox2 = RC4.get_Sbox_from_key(master_key)
	#Le offset est utilisé pour la concaténation finale des blocs en clair lors du déchiffrement 
	sub_blocs, offset = prep_bloc(texte)
	KL, KO, KI = prep_keys(master_key) #les sous clés sont en 16 bits
	sub_blocs_en = []

	#*------------------------*	
	#Première boucle pour parcourir les "blocs" de données de 64 bits
	for sub_bloc in sub_blocs:
		#left et right sont des entier de 32 bits
		left, right = split(sub_bloc, splitPos=32, blockSize=64) #left et right c'est 32
		#Deuxième boucle contenant l'algorithme kasumi		
		for iteration in range(8):
			temp = mainFunction(iteration, left, KO[iteration], KI[iteration] , KL[iteration] , Sbox1, Sbox2) ^ right #les clés sont des listes 3 * 16 bits en int
			right, left = left, temp
		sub_blocs_en.append(merge(left, right, rightNbOfBits=32))
	return [sub_blocs_en, offset]

def kasumi_encrypt_CBC(texte, master_key):
	#initialisation 
	Sbox1, Sbox2 = RC4.get_Sbox_from_key(master_key)
	sub_blocs, offset = prep_bloc(texte) 
	KL, KO, KI = prep_keys(master_key) 
	sub_blocs_en = []
	#Les valeurs du vecteur initial sont prises de manière arbitraire
	vecteur_initial = merge(merge(KL[3][0], KL[1][1], rightNbOfBits=16), merge(KL[6][1], KL[0][1], rightNbOfBits=16), rightNbOfBits=32) #pris de manière arbitrère

	#*------------------------*
	for sub_bloc in sub_blocs: 
		
		# XOR propre au CBC
		if sub_bloc == sub_blocs[0]:
			temp_bloc = vecteur_initial ^ sub_bloc
		else:
			temp_bloc = sub_blocs_en[-1] ^sub_bloc 

		# Algorithme kasumi appliqué au sub_bloc	
		left, right = split(temp_bloc, splitPos=32, blockSize=64)
		for iteration in range(8):
			temp = mainFunction(iteration, left, KO[iteration], KI[iteration] , KL[iteration] , Sbox1, Sbox2) ^ right #les clés sont des listes 3 * 16 bits en int
			right, left = left, temp
		sub_blocs_en.append(merge(left, right, rightNbOfBits=32))
	return [sub_blocs_en, offset]

def kasumi_encrypt_PCBC(texte, master_key):
	#initialisation 
	Sbox1, Sbox2 = RC4.get_Sbox_from_key(master_key)
	sub_blocs, offset = prep_bloc(texte) 
	KL, KO, KI = prep_keys(master_key) 
	sub_blocs_en = []
	vecteur_initial = merge(merge(KL[3][0], KL[1][1], rightNbOfBits=16), merge(KL[6][1], KL[0][1], rightNbOfBits=16), rightNbOfBits=32) #pris de manière arbitrère

	#*------------------------*
	for sub_bloc in sub_blocs:

		# XOR propre au PCBC
		if sub_bloc == sub_blocs[0]:
			temp_bloc = vecteur_initial ^ sub_bloc
		else:
			temp_bloc = bloc_retenu ^sub_bloc 
		
		# Algorithme kasumi appliqué au sub_bloc	
		left, right = split(temp_bloc, splitPos=32, blockSize=64) #left et right c'est 32
		for iteration in range(8):
			temp = mainFunction(iteration, left, KO[iteration], KI[iteration] , KL[iteration] , Sbox1, Sbox2) ^ right #les clés sont des listes 3 * 16 bits en int
			right, left = left, temp
		encrypted_bloc = merge(left, right, rightNbOfBits=32)

		# Ssauvegarde pour le XOR dans l'itération suivante
		bloc_retenu = encrypted_bloc ^ sub_bloc

		sub_blocs_en.append(encrypted_bloc)
	return [sub_blocs_en, offset]


