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

# Hashing Function - DJB2 for simplicity with some modification to make it work with gronsfeld cipher
def djb2(text):
    h = 5381
    magic_multiplier = 33
    hash_digest = ""
    for c in text:
        h = h * magic_multiplier + ord(c)
    for n in str(h):
        hash_digest = hash_digest + chr(int(n) + ord('A'))
    return hash_digest

# Authentication Flow - Sender
def authentication_scheme_sender(msg,key):
    msg = msg.upper()
    h = djb2(msg)
    packet = msg + "|" + h
    cipher = gronsfeld_encrypt(packet,key)
    return cipher

# Authentication Flow - Receiver
def authentication_scheme_receiver(cipher,key):
    packet = gronsfeld_decrypt(cipher,key)
    if "|" not in packet:
        return "Tampered"
    msg, h = packet.split("|")
    h_new = djb2(msg)
    if str(h_new) == h:
        return "Authentic"
    else:
        return "Tampered"

# Main Function
def main():
    # Example - Normal Plain Text
    plaintext = "HELLO"
    key = "123"

    ciphertext = gronsfeld_encrypt(plaintext,key)
    print("Cipher Text:", ciphertext)
    recovered = gronsfeld_decrypt(ciphertext,key)
    print("Plain Text obtained from the Cipher Text:",recovered)

    hashed_digest = djb2(plaintext)
    print("Hash Digest",hashed_digest)

    # Authentication demo
    cipher_packet = authentication_scheme_sender(plaintext, key)
    print("Cipher Packet:", cipher_packet)
    result = authentication_scheme_receiver(cipher_packet, key)
    print("Verification:", result)
    # Example for Tampering
    tampered = cipher_packet[:-1] + "X"
    print(authentication_scheme_receiver(tampered, key))

    # Example 2 - Plaintext with special Characters
    plaintext = "HELLO@123"
    key = "123"

    cipher_packet = authentication_scheme_sender(plaintext, key)
    print("Original Packet:", cipher_packet)

    # Receiver verifies normally
    print("Verification (original):", authentication_scheme_receiver(cipher_packet, key))

main()
    