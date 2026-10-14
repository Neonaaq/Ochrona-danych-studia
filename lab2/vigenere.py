import sys

def vigenere_szyfruj(dane: bytes, klucz: bytes):
    wynik = bytearray()
    klucz_len = len(klucz)
    for i, b in enumerate(dane):
        k_bajt = klucz[i % klucz_len]
        wynik.append((b + k_bajt) % 256)
    return bytes(wynik)

def vigenere_odszyfruj(dane: bytes, klucz: bytes):
    wynik = bytearray()
    klucz_len = len(klucz)
    for i, b in enumerate(dane):
        k_bajt = klucz[i % klucz_len]
        wynik.append((b - k_bajt) % 256)
    return bytes(wynik)

if len(sys.argv) < 2:
    print("Brakuje nazwy pliku.")
    sys.exit(1)

nazwa_pliku = sys.argv[1]
with open(nazwa_pliku, 'rb') as plik:
    dane = plik.read()

klucz = b"ZAMEK"

with open("vigenere.bin", "wb") as plikwy:
    plikwy.write(vigenere_szyfruj(dane, klucz))

with open("vigenere.bin", "rb") as plikwe:
    dane2 = plikwe.read()

dane2 = vigenere_odszyfruj(dane2, klucz)

if dane == dane2:
    print("Dane są OK")
else:
    print("Dane nie są takie same")

puste_dane = b""
zaszyfrowane_puste = vigenere_szyfruj(puste_dane, klucz)
odszyfrowane_puste = vigenere_odszyfruj(zaszyfrowane_puste, klucz)

if zaszyfrowane_puste != b"" or odszyfrowane_puste != b"":
    print("Błąd szyfrowania pustych danych")

dane_skrajne = b"\x00\xff\x00\xff"
zaszyfrowane_skrajne = vigenere_szyfruj(dane_skrajne, klucz)
odszyfrowane_skrajne = vigenere_odszyfruj(zaszyfrowane_skrajne, klucz)

if odszyfrowane_skrajne != dane_skrajne:
    print("Błąd danych z bajtem 0 i 255")

#####################################

tekst = b"BRAMABRAMABRAMA"
klucz1 = b"SZYFR"
klucz2 = b"KOD"

kryptogram1 = vigenere_szyfruj(tekst, klucz1)
kryptogram2 = vigenere_szyfruj(tekst, klucz2)

fragmenty1 = [kryptogram1[i:i+5].hex() for i in range(0, len(kryptogram1), 5)]
fragmenty2 = [kryptogram2[i:i+5].hex() for i in range(0, len(kryptogram2), 5)]

print(fragmenty1)
print(fragmenty2)