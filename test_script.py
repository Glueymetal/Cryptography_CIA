# Test Script — encrypt → hash → decrypt round trip
# Demonstrates Gronsfeld cipher and pearson hash working together

from gronsfeld import gronsfeld_encrypt, gronsfeld_decrypt
from pearson import pearson_hash
from authentication import authentication_scheme_sender, authentication_scheme_receiver


def test_cipher(plaintext, key):
    print("=" * 50)
    print(f"Plaintext        : {plaintext}")
    print(f"Key              : {key}")
    ciphertext = gronsfeld_encrypt(plaintext, key)
    print(f"Ciphertext       : {ciphertext}")
    recovered = gronsfeld_decrypt(ciphertext, key)
    print(f"Recovered        : {recovered}")
    assert recovered == plaintext.upper(), "Decrypt failed!"
    print("Cipher Round Trip: Passed")


def test_hash(plaintext):
    print("-" * 50)
    h = pearson_hash(plaintext.upper())
    print(f"Hash of '{plaintext}': {h}")


def test_authentication(plaintext, key):
    print("-" * 50)
    print(f"Authentication Test — Plaintext: '{plaintext}', Key: '{key}'")

    # Normal flow
    cipher_packet = authentication_scheme_sender(plaintext, key)
    print(f"Cipher Packet    : {cipher_packet}")
    result = authentication_scheme_receiver(cipher_packet, key)
    print(f"Verification     : {result}")

    # Tampered flow
    tampered = cipher_packet[:-1] + "X"
    print(f"Tampered Packet  : {tampered}")  # <-- Add this line
    tampered_result = authentication_scheme_receiver(tampered, key)
    print(f"Tampered Result  : {tampered_result}")


def main():
    # Example 1 — Plain alphabetic text
    test_cipher("HELLO", "123")
    test_hash("HELLO")
    test_authentication("HELLO", "123")

    print()

    # Example 2 — Text with special characters
    test_cipher("HELLO@WORLD", "456")
    test_hash("HELLO@WORLD")
    test_authentication("HELLO@WORLD", "456")


main()