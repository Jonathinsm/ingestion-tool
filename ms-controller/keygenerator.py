from cryptography.fernet import Fernet
key = Fernet.generate_key()
print (key)

file = open('key.ley', 'wb')
file.write(key)