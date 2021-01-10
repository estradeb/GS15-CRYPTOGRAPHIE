from pyfinite import ffield


def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def split(bloc, splitPos=16, blockSize=32): 
	# bloc est en base 10
	# split à la position 16 un block de 32 par défaut 
	bloc = bin(bloc)[2:].zfill(blockSize)
	left = bloc[:splitPos]
	right = bloc[splitPos:]
	left = int(left , 2)
	right = int(right , 2)
	return left, right #ressort ici en base 10
	

def merge(left, right, rightNbOfBits):
	result = bin(left)[2:] + bin(right)[2:].zfill(rightNbOfBits)
	return int(result, 2)

def inversion_I(a):
	F = ffield.FField(15)
	a_inverse = F.Inverse(a)
	return a_inverse 


def forgeBinary(number, size=32):
	return bin(number)[2:].zfill(size)[-size:] #zfill pour le padding et [-size:] pour s'assurer que le bloc 32 de taille

def rightRotation(number, numberOfBits=2 ,size=32):
	binNumber = forgeBinary(number, size)
	binNumber =  binNumber[-numberOfBits:]+binNumber[:-numberOfBits]
	return int(binNumber, 2)
def leftRotation(number, numberOfBits=1 ,size=16):
	binNumber = forgeBinary(number, size)
	binNumber =  binNumber[numberOfBits:]+binNumber[:numberOfBits]
	return int(binNumber, 2)

def countOffset(string):
	offset = 0
	while int(string[offset],2) == 0:
		offset += 1
	return offset

def addition_mod32(a, b):	
	return (a + b) % 4294967296

def divide_bitwise(number, blocSize, min_number_of_blocks=0):
	blocks = []
	while number != 0:
		blocks.append(number & int('1'*blocSize,2))
		number = number >> blocSize

	# Ceci assure qu'aux cas où numbre est trop petit, le nombre de bloc reste le meme
	# Pour SHA_1 on souhaite 16 mots de 32 bits
	# si number est trop petit, il y aura quand même 16 mots avec quelque mots nuls
	while len(blocks) <= min_number_of_blocks:
		blocks.append(0)
	return blocks