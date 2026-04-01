from gronsfeld import gronsfeld_encrypt, gronsfeld_decrypt
from pearson import pearson_hash

# Authentication Flow - Sender
def authentication_scheme_sender(msg,key):
    msg = msg.upper()
    h = pearson_hash(msg)
    packet = msg + "|" + h
    cipher = gronsfeld_encrypt(packet,key)
    return cipher

# Authentication Flow - Receiver
def authentication_scheme_receiver(cipher,key):
    packet = gronsfeld_decrypt(cipher,key)
    if "|" not in packet:
        return "Tampered"
    msg, h = packet.split("|")
    h_new = pearson_hash(msg)
    if str(h_new) == h:
        return "Authentic"
    else:
        return "Tampered"