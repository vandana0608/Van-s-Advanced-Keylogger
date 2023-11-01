from cryptography.fernet import Fernet
#Use encryption key that is generated in encryption_key.txt for decryption
key = "w4eLP7fMuJwYoRJyqbpfkn2LSQNWYiDNy2KooG26SSE="
#Encrypted file paths
system_information_e = '/Users/van/Documents/UNSW/Courses/Year 1/Y1 Term 3/COMP6441 - Security Engineering/UNSW-T3-COMP6441/Assignments/Final Deliverable/Advanced Keylogger/e_systeminfo.txt'
keys_information_e = '/Users/van/Documents/UNSW/Courses/Year 1/Y1 Term 3/COMP6441 - Security Engineering/UNSW-T3-COMP6441/Assignments/Final Deliverable/Advanced Keylogger/e_key_log.txt'
encrypted_files = [system_information_e, keys_information_e]
count = 0
for decrypting_files in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    with open("/Users/van/Documents/UNSW/Courses/Year 1/Y1 Term 3/COMP6441 - Security Engineering/UNSW-T3-COMP6441/Assignments/Final Deliverable/Advanced Keylogger/decryption.txt", 'ab') as f:
        f.write(decrypted)
    count += 1