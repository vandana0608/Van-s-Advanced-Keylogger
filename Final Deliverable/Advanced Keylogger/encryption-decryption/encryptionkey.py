from cryptography.fernet import Fernet
#Generate fernet key that will be used to decrypt ciphertext
key = Fernet.generate_key()
#Encrypted file path (P.S put in your custom folder path)
file = open("/Users/van/Documents/UNSW/Courses/Year 1/Y1 Term 3/COMP6441 - Security Engineering/UNSW-T3-COMP6441/Assignments/Final Deliverable/Advanced Keylogger/encryption-decryption/encryption_key.txt", 'wb')
file.write(key)
file.close()