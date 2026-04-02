# Cryptograhpy CIA

#### Name: Jeyashree Muthukumaran
#### Class: IoT A
#### Reg No: 23011102033

---
# Gronsfeld Cipher + Pearson Hash — Message Authentication
---

## Overview

This project implements the **Gronsfeld Cipher** for encryption and decryption, paired with the **Pearson Hashing Algorithm** for message authentication. Together, they form a lightweight scheme where the sender encrypts both the message and its hash, and the receiver verifies that nothing was tampered with by recomputing the hash after decryption.

---

## Theory

### Gronsfeld Cipher

The Gronsfeld cipher is a polyalphabetic substitution cipher — essentially a restricted version of the Vigenère cipher where the key is made up of digits (0–9) rather than letters. Each digit in the key acts as a shift for the corresponding character in the plaintext, cycling through the key if it's shorter than the message.

**Encryption:**
```
C = (P - base + shift) mod 26 + base
```

**Decryption:**
```
P = (C - base - shift) mod 26 + base
```

Here, `base` is the ASCII value of `'A'` (65), and `shift` is the current key digit.

**Key cycling:** If the key is shorter than the message, it wraps around. For example, key `"123"` applied to `"HELLO"` becomes `"12312"`.

**Implementation assumptions:**
- Only uppercase letters are shifted; everything else (digits, punctuation, spaces) passes through unchanged.

---

### Pearson Hash Function

The Pearson hash is a fast, table-driven, non-cryptographic hash function first described by Peter Pearson in 1990. It was chosen for this project because it is straightforward to implement from scratch without any external libraries, and it produces a compact, consistent digest suitable for integrity checking alongside a lightweight cipher like Gronsfeld.

**Why Pearson?**

The Pearson hash was chosen because it pairs naturally with the Gronsfeld cipher at every level. It is implemented entirely from scratch using a fixed permutation table and XOR operations — no libraries, no complex bit manipulation. The output is a compact hex string (digits 0–9 and letters A–F), which slots cleanly into the cipher packet: digits pass through the Gronsfeld cipher unchanged, and hex letters shift and unshift correctly along with the rest of the message. This means the hash digest can be embedded directly without any extra encoding. The algorithm is also deterministic and sensitive to input changes, which is exactly what an integrity check needs.

**How it works:**

1. A 256-byte permutation table is generated once at startup using a fixed seed string (`"pearson1990"`).
2. For each output byte at position `byte_index`, the hash is computed as:

```
h = TABLE[(ord(text[0]) + byte_index) % 256]
for each subsequent character c:
    h = TABLE[h XOR ord(c)]
```

3. The resulting bytes are assembled into a single integer and returned as a zero-padded hex string.

**Default digest size:** 4 bytes → 8 hex characters (e.g., `A3F10C2B`).

---

## Authentication Scheme

The scheme follows a **Hash-then-Encrypt** approach.

### Sender
```
1. M  ← plaintext.upper()
2. H  ← PEARSON_HASH(M)
3. P  ← M + "|" + H
4. C  ← GRONSFELD_ENCRYPT(P, K)
5. Transmit C
```

### Receiver
```
1. P       ← GRONSFELD_DECRYPT(C, K)
2. M, H    ← SPLIT(P, delimiter="|")
3. H'      ← PEARSON_HASH(M)
4. if H' == H  → Authentic
   else        → Tampered
```

---

## File Structure

```
project/
├── gronsfeld.py            ← Gronsfeld encrypt and decrypt
├── pearson.py              ← Pearson hash function
├── authentication.py       ← Sender and receiver logic
├── test_script.py          ← Round-trip test script
├── Test Script Output.docx ← Screenshot of the Output of 2 Examples
└── README.md               ← This file
```

---

## How to Run

Make sure all files are in the same directory. No external libraries are required — this is pure Python.

```bash
python test_script.py
```

The test script will print results for each of the four demonstration steps described below.

---

## Worked Examples

### Example 1 — Plain Alphabetic Text

| Step | Value |
|---|---|
| Plaintext | `HELLO` |
| Key | `123` |
| Ciphertext | `IGOMQ` |
| Hash Digest | 8-character hex (e.g. `A3F10C2B`) |
| Cipher Packet | `HELLO\|<hash>` |
| Encrypted Packet | `IGOMQ\|<encrypted hash>` |
| Verification | Authentic ✓ |
| Tampered Verification | Tampered ✗ |

**How the shift works for HELLO with key 12312:**

| Char | Shift | Result |
|------|-------|--------|
| H | +1 | I |
| E | +2 | G |
| L | +3 | O |
| L | +1 | M |
| O | +2 | Q |

> The exact hash value depends on the permutation table seeded by `"pearson1990"`. Run `test_script.py` to see live output.

---

### Example 2 — Text with Special Characters

| Step | Value |
|---|---|
| Plaintext | `HELLO@WORLD` |
| Key | `456` |
| Ciphertext | `LJRPT@CSWRH` |
| Hash Digest | 8-character hex |
| Encrypted Packet | `LJRPT@CSWRH\|<encrypted hash>` |
| Verification | Authentic ✓ |
| Tampered Verification | Tampered ✗ |

The `@` symbol is not an uppercase letter, so it passes through the cipher unchanged — consistent with the implementation assumption that only alphabetic characters are shifted.

---

## Test Script — What It Demonstrates

The test script (`test_script.py`) walks through four scenarios:

1. **Cipher round-trip** — encrypting then decrypting a message recovers the original plaintext exactly.
2. **Hash consistency** — the Pearson hash produces the same 8-character hex digest every time for the same input.
3. **Normal authentication flow** — the receiver correctly verifies an unmodified encrypted packet.
4. **Tampered packet detection** — prints the tampered packet and shows that the receiver correctly flags it as modified.

---

## Complexity

| Component | Time | Space |
|---|---|---|
| Gronsfeld Encrypt / Decrypt | O(n) | O(n) |
| Pearson Hash | O(n × d) | O(1) |
| Authentication Scheme | O(n) | O(n) |

`n` is the length of the message. `d` is the digest size in bytes (default: 4). The permutation table is fixed at 256 entries, so it contributes O(1) space regardless of input size.
