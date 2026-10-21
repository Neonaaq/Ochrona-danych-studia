import math
from collections import Counter
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def oblicz_entropie(dane: bytes):
    if not dane:
        return 0.0
    licznik = Counter(dane)
    dlugosc = len(dane)
    entropia = 0.0
    for count in licznik.values():
        p = count / dlugosc
        entropia -= p * math.log2(p)
    return entropia

alfabet = "abcdefghijklmnopqrstuvwxyz0123456789"

with open("slaby_ecb.bin", "rb") as f:
    kryptogram = f.read()

if kryptogram:
    wyniki = []
    probka = kryptogram[:4096]

    for znak in alfabet:
        klucz = (znak * 16).encode('utf-8')

        cipher = AES.new(klucz, AES.MODE_ECB)
        odszyfrowana_probka = cipher.decrypt(probka)

        h = oblicz_entropie(odszyfrowana_probka)
        wyniki.append((znak, h, klucz))

    wyniki.sort(key=lambda x: x[1])

    top_5 = wyniki[:5]
    for znak, h, _ in top_5:
        print(f"Znak klucza: '{znak}'  Entropia H: {h:.4f}")

    najlepszy_znak, najlepsza_h, najlepszy_klucz = wyniki[0]

    cipher_full = AES.new(najlepszy_klucz, AES.MODE_ECB)
    odszyfrowane_pelne = unpad(cipher_full.decrypt(kryptogram), AES.block_size)

    pierwszy_wiersz = odszyfrowane_pelne.split(b'\n')[0].decode('utf-8')

    print(f"\nZnak klucza: '{najlepszy_znak}'")
    print(f"Pierwszy wiersz tekstu: {pierwszy_wiersz}")