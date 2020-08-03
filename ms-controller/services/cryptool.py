from cryptography.fernet import Fernet

def read_key():
    file = open('key.ley', 'rb')
    key = file.read()
    file.close()
    return key

def encrpyt(data):
    key = read_key()
    encoded_data = data.encode()
    f = Fernet(key)
    encrypted = f.encrypt(encoded_data)
    encrypted_decoded_data = encrypted.decode()
    return encrypted_decoded_data

def decrpyt(data):
    key = read_key()
    encoded_data = data.encode()
    f = Fernet(key)
    decrpyted = decrpyted = f.decrypt(encoded_data)
    decrpyted_decoded_data = decrpyted.decode()
    return decrpyted_decoded_data