import sys

def cezar_odszyfruj(dane: bytes, klucz: int):
    return bytes((b - klucz) % 256 for b in dane)

def udzial_bajtow(tekst: bytes):
    if not tekst:
        return 0.0

    dozwolone_znaki = set(range(32, 127)) | {9, 10, 13}
    poprawne_znaki = sum(1 for b in tekst if b in dozwolone_znaki)

    return poprawne_znaki / len(tekst)

if len(sys.argv) < 2:
    print("Brakuje nazwy pliku.")
    sys.exit(1)

nazwa_pliku = sys.argv[1]
with open(nazwa_pliku, 'rb') as plik:
    dane = plik.read()

wyniki = []
for k in range(256):
        probka = cezar_odszyfruj(dane, k)
        c = udzial_bajtow(probka)
        wyniki.append((c, k, probka))

wyniki.sort(key = lambda x: (-x[0], x[1]))

for i in range(5):
    c, k, probka = wyniki[i]
    print(f"{i+1}. {c} \t {k} \t {probka[:50]}")

nr = input("Podaj numer kandydata (1-5): ")
nr = int(nr) - 1
key = wyniki[nr][1]
with open('cezar.txt', 'wb') as plik:
    plik.write(cezar_odszyfruj(dane, key))
