import math
from collections import Counter
import itertools
import time
import sys

def oblicz_entropie(dane: bytes) -> float:
    if not dane:
        return 0.0
    zliczanie = Counter(dane)
    dlugosc = len(dane)
    entropia = 0.0
    for count in zliczanie.values():
        p = count / dlugosc
        entropia -= p * math.log2(p)
    return entropia

def rc4_generuj_strumień(klucz: bytes, dlugosc: int) -> bytes:
    # KSE
    S = list(range(256))
    j = 0
    key_length = len(klucz)

    for i in range(256):
        j = (j + S[i] + klucz[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA
    i = 0
    j = 0
    strumien = bytearray()
    for _ in range(dlugosc):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        strumien.append(K)

    return bytes(strumien)

def rc4_kryptuj(dane: bytes, klucz: bytes) -> bytes:
    strumien = rc4_generuj_strumień(klucz, len(dane))
    # XOR
    return bytes(d ^ k for d, k in zip(dane, strumien))

if len(sys.argv) < 2:
    print("Brakuje nazwy pliku.")
    sys.exit(1)

nazwa_pliku = sys.argv[1]
with open(nazwa_pliku, 'rb') as plik:
    dane = plik.read()

# testowanie dwukrotnego zastosowania
klucz = b"abc"
dane2 = rc4_kryptuj(dane, klucz)
if dane != rc4_kryptuj(dane2, klucz):
    print("Błąd z dwukrotnym zastosowaniem")

# generowanie wszystkich kluczy
alfabet = "abcdefghijklmnopqrstuvwxyz"
wszystkie_klucze = [bytes("".join(p), "ascii") for p in itertools.product(alfabet, repeat=3)]

start = time.time()
probka_len = min(512, len(dane))
probka = dane[:probka_len]

wyniki = []
for klucz_probny in wszystkie_klucze:
    odszyfrowana_probka = rc4_kryptuj(probka, klucz_probny)
    entropia = oblicz_entropie(odszyfrowana_probka)
    wyniki.append((entropia, klucz_probny))

stop = time.time()
czas = stop - start

# sortowanie rosnąco, przy remisie kolejność alfabetyczna
wyniki.sort(key=lambda x: (x[0], x[1]))

print("Najlepsi kandydaci:\n")
for i in range(5):
    ent, k_bytes = wyniki[i]
    print(f"{i+1}. Klucz: {k_bytes.decode('ascii')} | Entropia: {ent:.4f}")

_, najlepszy_klucz = wyniki[0]
tekst = rc4_kryptuj(dane, najlepszy_klucz)
if rc4_kryptuj(tekst, najlepszy_klucz) != dane:
    "Błąd z ponownym szyfrowaniem"

with open('rc4.txt', 'wb') as plik:
    plik.write(tekst)

print(f"Liczba prób: {len(wszystkie_klucze)}")
print(f"Czas przeszukiwania: {czas:.3f} s")
print(f"Entropia całego kryptogramu: {oblicz_entropie(dane):.4f}")
print(f"Entropia całego odszyfrowania: {oblicz_entropie(tekst):.4f}")
