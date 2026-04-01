def _build_table():
    perm = list(range(256))
    seed = list(b"pearson1990")
    j = 0
    for i in range(256):
        j = (j + perm[i] + seed[i % len(seed)]) % 256
        perm[i], perm[j] = perm[j], perm[i]
    return perm
 
_TABLE = _build_table()
 
def pearson_hash(text: str, digest_bytes: int = 4) -> str:
    result = 0
    for byte_index in range(digest_bytes):
        h = _TABLE[(ord(text[0]) + byte_index) % 256] if text else 0
        for c in text[1:]:
            h = _TABLE[h ^ ord(c)]
        result = (result << 8) | h
    return format(result, f'0{digest_bytes * 2}X')