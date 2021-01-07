def forgeBinary(number, size=32):
	return bin(number)[2:].zfill(size)[-size:] #zfill pour le padding et [-size:] pour s'assurer que le bloc 32 de taille

def rightRotation(number, offset=2 ,size=32):
	binNumber = forgeBinary(number, size)
	binNumber =  binNumber[-offset:]+binNumber[:-offset]
	return int(binNumber, 2)
def leftRotation(number, offset=1 ,size=32):
	binNumber = forgeBinary(number, size)
	binNumber =  binNumber[offset:]+binNumber[:offset]
	return int(binNumber, 2)

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

