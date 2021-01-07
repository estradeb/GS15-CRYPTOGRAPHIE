from tools import *

K = [0] * 80
for t in range(20):	K[t] = 0x5A827999 
for t in range(20 ,40) : K[t] = 0x6ED9EBA1 
for t in range(40 ,60) : K[t] = 0x8F1BBCDC 
for t in range(60 ,80) : K[t] = 0xAC52C1D5 

H = [0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0]

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
	x = x << 1 | 1 
	# step 2
	blocks = []
	iteration = 1
	while x != 0:
		offset = (x.bit_length() - 512*iteration) if (x.bit_length() - 512*iteration) > 0 else 0
		blocks.append(x >> (offset))
		# del 512 MSB si c'est possible
		if bin(x)[512 + 2:] != '':
			x = int(bin(x)[512 + 2:] ,2)
		else :	
			break
		iteration = iteration + 1

	#padding des LSB pour avoir 512 bits
	# Test, est-ce qu'on a la place pour la longueur ? 
	# Cas où il n'y pas la place
	if 512 - blocks[-1].bit_length() <= 64:
		blocks[-1] = blocks[-1] << (512 - blocks[-1].bit_length())
		blocks.append(longueur << (512 - longueur.bit_length())) # ici padding illegal, on met longueur en MSB pour avoir un bloc de 512 bits
	
	# Cas où il y a la place
	else:
		blocks[-1] = blocks[-1] << (512 - blocks[-1].bit_length())
		blocks[-1] = blocks[-1] | longueur
	return blocks

def ft(B,C,D):
	x = [0] * 80
	for t in range(20) : x[t] = (B & C) | (~B & D)
	for t in range(20,40) :x[t] = B ^ C ^ D  
	for t in range(40,60) : x[t] = (B & C) | (B & D) | (C & D) 
	for t in range(60,80) : x[t] = B ^ C ^ D
	return x


def SHA_1(data):
	blocks = prep_data(data)
	for block in blocks:
		# etape 1
		x = divide_bitwise(block, blocSize=32)
		# etape 2
		for t in range(16,80):
			x.append(leftRotation(x[t-3] ^ x[t-8] ^ x[t-14] ^ x[t-16]))

		# etape 3
		A, B, C, D, E = H
		# etape 4
		temp = ft(B,C,D)
		for t in range(80):
			T = (((leftRotation(A, offset=5 ,size=32) + temp[t]) % 4294967296 + E ) % 4294967296 + x[t]  % 4294967296 + K[t] ) % 4294967296
			E=D
			D=C
			C = leftRotation(B, offset=30 ,size=32)
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



# data = " macron démission macron destructionmacron démission macron destructionmacron démission macron destructionmacron démission  mac"

# print(SHA_1(data))
'''
retourne 160 bits
'''