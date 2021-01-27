from ressources.tools import *

def prep_data(data):
	# Determine le type de data pour le traiter
	if isinstance(data, str):
		x = ''
		for n in range(len(data)):
			x +='{0:08b}'.format(ord(data[n]))
		#calcul de la longueur avant l'étape 1
		longueur = len(x)
		x = int(x,2)
		#step 1
	elif isinstance(data, int):
		x = data
		longueur = x.bit_length()

	# step 1, ajout d'un 1 à la fin
	x = x << 1 | 1 

	# step 2	
	# Calcul de k, le nombre d'information à rajouter tel que le message soit un multiple de 512 bits facilement découpable
	k = (448 - longueur - 1) % 512
	# Insertion de la longueur sur les 64 LSB
	x = x << (k + 64) | longueur
	blocks = divide_bitwise(number=x, blocSize=512)
	return blocks

def ft(B,C,D):
	x = [0] * 80
	for t in range(20) : x[t] = (B & C) | (~B & D)
	for t in range(20,40) :x[t] = B ^ C ^ D  
	for t in range(40,60) : x[t] = (B & C) | (B & D) | (C & D) 
	for t in range(60,80) : x[t] = B ^ C ^ D
	return x


def SHA_1(data):
	K = [0] * 80
	for t in range(20):	K[t] = 0x5A827999 
	for t in range(20 ,40) : K[t] = 0x6ED9EBA1 
	for t in range(40 ,60) : K[t] = 0x8F1BBCDC 
	for t in range(60 ,80) : K[t] = 0xAC52C1D5 

	H = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]

	blocks = prep_data(data)
	for block in blocks:
		# etape 1
		x = divide_bitwise(block, blocSize=32, min_number_of_blocks = 16)
		# etape 2
		for t in range(16,80):
			x.append(leftRotation(x[t-3] ^ x[t-8] ^ x[t-14] ^ x[t-16], size=32))

		# etape 3
		A, B, C, D, E = H
		# etape 4
		temp = ft(B,C,D)
		for t in range(80):
			T = (((leftRotation(A, numberOfBits=5 ,size=32) + temp[t]) % 4294967296 + E ) % 4294967296 + x[t]  % 4294967296 + K[t] ) % 4294967296
			E=D
			D=C
			C = leftRotation(B, numberOfBits=30 ,size=32)
			B=A
			A=T

		# etape 5
		H[0] = addition_mod32(H[0], A)
		H[1] = addition_mod32(H[1], B)
		H[2] = addition_mod32(H[2], C)
		H[3] = addition_mod32(H[3], D)
		H[4] = addition_mod32(H[4], E)
		
	result = 0
	for i in H:
		result = result << 32 | i
	return result


