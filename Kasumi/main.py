from chiffrement import *
from dechiffrement import *

f=open("clear.txt", "r")
if f.mode == 'r':
	content =f.read()

key = 'GS15 est une très bon UE maintenant'
encrypted_content = kasumi_encrypt_ECB(content, key)


with open('encrypted_content.txt', 'w') as f:
    f.write("%s\n" % encrypted_content)

decrypted_content = kasumi_decrypt_ECB(encrypted_content, key)
print(decrypted_content)
with open('decrypted_content.txt', 'w') as f:
    f.write("%s\n" % decrypted_content)
