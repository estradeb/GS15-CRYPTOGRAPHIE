import random
import string
import main.kasumi.kasumi_tools as kt
import ressources.tools as tls

def RC4(key, input):
	n = len(key)
	R = list(range(256)) #table de permute Integer
	j = 0

	for i in range(256):
		j = j + R[i] + ord(key[i%n]) & 0xFF
		#print('j =  ',j,' R[i] = ',R[i],', key[i%n] = ', ord(key[i%n]))
		R[i], R[j] = R[j] , R[i]

	j , i = 0 , 0
	output = [None]*len(input)
	for l in range(len(input)):
		i = (i+1) & 0xFF
		j = (j+R[i]) & 0xFF
		R[i], R[j] = R[j] , R[i]
		output[l] = (ord(input[l]) ^ R[(R[i] + R[j])&0xFF])
	return output #''.join(output)

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_RC4_Sbox(length):
	x, y = get_random_string(length), get_random_string(length)
	return RC4(x, y)

def get_Sbox_from_key(key):
	#initialisation
	KL, KO, KI = kt.prep_keys(key)
	temp = 0
	C = [37144, 22549, 2172, 25078, 407, 20225, 38393, 47277]

	 #*----------------------*
	for sub_key in KL:
		for item in sub_key:
			temp = tls.merge(temp, item, 16)
	for sub_key in KO:
		for item in sub_key:
			temp = tls.merge(temp, item, 16)
	for sub_key in KI:
		for item in sub_key:
			temp = tls.merge(temp, item, 16)
	key1 =  str(temp)[:256]

	for sub_key in KO:
		for item in sub_key:
			temp = tls.merge(temp, item, 16)
	for sub_key in KI:
		for item in sub_key:
			temp = tls.merge(temp, item, 16)
	for sub_key in KL:
		for item in sub_key:
			temp = tls.merge(temp, item, 16)
	key2 = str(temp)[:256]
	
	return RC4(key1, key2), RC4(key2,key1)

	
