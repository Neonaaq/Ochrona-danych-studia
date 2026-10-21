from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

tekst = b"0123456789ABCDEF" * 4
klucz = bytes.fromhex("000102030405060708090a0b0c0d0e0f")

iv = get_random_bytes(16)

cipher_ecb = AES.new(klucz, AES.MODE_ECB)
cipher_cbc = AES.new(klucz, AES.MODE_CBC, iv)

kryptogram_ecb = cipher_ecb.encrypt(tekst)
kryptogram_cbc = cipher_cbc.encrypt(tekst)

print("\n ===== ecb =====")
bloki_ecb = [kryptogram_ecb[i:i+16] for i in range(0, len(kryptogram_ecb), 16)]
for blok in bloki_ecb:
    print(f"{blok.hex()}")

print("\n ===== cbc =====")
bloki_cbc = [kryptogram_cbc[i:i+16] for i in range(0, len(kryptogram_cbc), 16)]
for blok in bloki_cbc:
    print(f"{blok.hex()}")

decipher_ecb = AES.new(klucz, AES.MODE_ECB)
decipher_cbc = AES.new(klucz, AES.MODE_CBC, iv)

odszyfrowane_ecb = decipher_ecb.decrypt(kryptogram_ecb)
odszyfrowane_cbc = decipher_cbc.decrypt(kryptogram_cbc)

if odszyfrowane_ecb == odszyfrowane_cbc == tekst:
    print("\nOdszyfrowane poprawnie obydwa")



