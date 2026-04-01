# Encryption and Decryption done using Gronsfeld cipher
# Assumptions :- 1) Only deals with Capital Letters
#                2) Special Characters will be appended as it is

def gronsfeld_encrypt(text,key):
    text = text.upper() 
    ciphertext = ""

    alpha_count = sum(1 for c in text if c.isalpha())
    while len(key) < alpha_count:
        key += key
    
    key_index = 0

    for i in range(len(text)):
        c = text[i]
        if c.isalpha():
            shift = int(key[key_index])
            key_index += 1
            base = ord('A')
            ciphertext = ciphertext + chr((ord(c) - base + shift) % 26 + base)
        else:
            ciphertext = ciphertext + c
    
    return ciphertext

def gronsfeld_decrypt(ciphertext,key):
    plaintext = ""

    alpha_count = sum(1 for c in ciphertext if c.isalpha())
    while len(key) < alpha_count:
        key += key
    
    key_index = 0

    for i in range(len(ciphertext)):
        c = ciphertext[i]
        if c.isalpha():
            shift = int(key[key_index])
            key_index += 1
            base = ord('A')
            plaintext = plaintext + chr((ord(c) - base - shift) % 26 + base)
        else:
            plaintext = plaintext + c
    
    return plaintext