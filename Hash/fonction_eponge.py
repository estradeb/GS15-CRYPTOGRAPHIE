import math
from tools import *
from SHA_1 import *

def eponge(data):
	etat = 0
	r_length = 80
	c_length = 160 - r_length
	
	# Conversion en int
	if isinstance(data, str):
		message = ''
		for n in range(len(data)):
			message +='{0:08b}'.format(ord(data[n]))
		message = int(message,2)
	#*---------------*
	# Absorption
	blocs = []
	blocs = divide_bitwise(padding(message, r_length), blocSize=r_length)
	for bloc in blocs:
		capacity = etat & int('1'*c_length,2) #la capacité est en LSB
		bit_rate = etat >> c_length #le bit_rate est en MSB
		etat = SHA_1((bit_rate ^ bloc) << c_length | capacity)

	#*---------------*
	# Essorage
	sortie = 0
	for iteration in range(len(blocs)):
		# Concaténation de des bit_rates
		sortie = sortie << r_length | (etat >> c_length) 
		état = SHA_1(etat)
	return sortie

def padding(message, r_length):
	k = math.ceil(message.bit_length() / r_length)
	padding = r_length * int(k)
	# on ajoute un 1 puis les zéros à la suite
	return (message << 1 | 1 ) << (padding  - message.bit_length() - 1)


