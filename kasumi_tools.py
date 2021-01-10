from tools import *
from math import ceil

def FL(bloc, KL): 
	left,  right = split(bloc, 16)
	#translates a 32-bit input to a 32-bit output using a subkey is split into two 16-bit subkeys,  KLi,1 and KLi,2 where.
	rightd = inversion_I(right ^ (leftRotation(left & KL[0], numberOfBits=1 ,size=16))) 
	leftd = inversion_I(left ^ (leftRotation(rightd | KL[1], numberOfBits=1 ,size=16)))
	#KL devrait avoir deux parties différentes ici mais les dimensions ne collent pas
	return merge(rightd,leftd, 16)

def FI(bloc, KI, Sbox1, Sbox2): #attention le KI ici est de 16 bits
	KI1, KI2 = split(KI, splitPos=8, blockSize = 16)
	return rightRotation(bloc,numberOfBits=2, size=16) ^ merge(Sbox1[KI1], Sbox2[KI2], rightNbOfBits=8)

def FO(bloc, KO, KI, Sbox1, Sbox2):
	# translates a 32-bit input to a 32-bit output using two 48-bit subkeys.
	left, right = split(bloc, 16) #2 * 16 bits

	#Itération 1
	left1 = right
	right1 = right ^ (FI(left ^ KO[0], KI[0], Sbox1, Sbox2)) #left et KO[0] sont 16 bits
	#Itération 2
	left2 = right1
	right2 = right1 ^ (FI(left1 ^ KO[1], KI[1], Sbox1, Sbox2))
	#Itération 3
	left3 = right2
	right3 = right2 ^ (FI(left2 ^ KO[2], KI[2], Sbox1, Sbox2))
	return merge(left3, right3, 16)

def prep_bloc(bloc, blockSize=64): #prend un texte brut
	# bloc = text_to_bits(base64_encode(bloc))
	bloc = text_to_bits((bloc))
	sub_blocs = []
	offset = []
	for j in range(ceil(len(bloc)/blockSize)): #itération par bloc de 64 bits
		string = bloc[j*blockSize:(j+1)*blockSize]
		offset.append(countOffset(string))
		sub_blocs.append(int(string,2)) #découpage des blocs de 64 bits et conversion en entier
	# temp = sub_blocs.pop(-1) 
	# sub_blocs.append(padding(temp, requieredSize=64)) #padding sur le dernier bloc
	return sub_blocs, offset

def prep_keys(master_key):
	#Fait les sub key K
	master_key = text_to_bits(master_key)
	K = []
	for x in range(8):
		K.append(int(master_key[x*16:(x+1)*16],2))
	#Fait les sub key K'
	C = [ 291, 17767, 35243, 52719, 65244, 47768, 30292, 12816]	 #base 10 de l'original
	Kd = []
	for j in range(8):
		Kd.append(C[j]^K[j])

	#Key schedule copiée sur la norme donnée dans l'énoncé
	KL = []
	KO = []
	KI = []

	KL.append([leftRotation(K[0], 1), leftRotation(K[1], 1), leftRotation(K[2], 1), leftRotation(K[3], 1), leftRotation(K[4], 1), leftRotation(K[5], 1), leftRotation(K[6], 1), leftRotation(K[7], 1)])
	KL.append([Kd[(3-1)],Kd[(4-1)],Kd[(5-1)],Kd[(6-1)],Kd[(7-1)],Kd[(8-1)],Kd[(1-1)],Kd[(2-1)]])

	KO.append([leftRotation(K[1], 5), leftRotation(K[2], 5), leftRotation(K[3], 5), leftRotation(K[4], 5), leftRotation(K[5], 5), leftRotation(K[6], 5), leftRotation(K[7], 5), leftRotation(K[0], 5)])
	KO.append([leftRotation(K[5], 8), leftRotation(K[6], 8), leftRotation(K[7], 8), leftRotation(K[0], 8), leftRotation(K[1], 8), leftRotation(K[2], 8), leftRotation(K[3], 8), leftRotation(K[4], 8)])
	KO.append([leftRotation(K[6], 13), leftRotation(K[7], 13), leftRotation(K[0], 13), leftRotation(K[1], 13), leftRotation(K[2], 13), leftRotation(K[3], 13), leftRotation(K[4], 13), leftRotation(K[5], 13)])

	KI.append([Kd[(5-1)],Kd[(6-1)],Kd[(7-1)],Kd[(8-1)],Kd[(1-1)],Kd[(2-1)],Kd[(3-1)],Kd[(4-1)]])
	KI.append([Kd[(4-1)],Kd[(5-1)],Kd[(6-1)],Kd[(7-1)],Kd[(8-1)],Kd[(1-1)],Kd[(2-1)],Kd[(3-1)]])
	KI.append([Kd[(8-1)],Kd[(1-1)],Kd[(2-1)],Kd[(3-1)],Kd[(4-1)],Kd[(5-1)],Kd[(6-1)],Kd[(7-1)]])

	#Petite combine pour transposer ces listes (c'est plus pratique comme ça)
	KL = list(map(list, zip(*KL))) 
	KO = list(map(list, zip(*KO))) 
	KI = list(map(list, zip(*KI))) 

	return KL, KO, KI
 
def mainFunction(iteration, left, KO, KI, KL, Sbox1, Sbox2):
	#prend un bloc left i-1 donc 32 bits en théorie
	if (iteration+1)%2==1:  #cas impaire, le "+1" sert à s'y retrouver dans les listes
		return FO(FL(left, KL), KO, KI, Sbox1, Sbox2)
	else:
		return FL(FO(left, KO, KI, Sbox1, Sbox2) ,KL)

