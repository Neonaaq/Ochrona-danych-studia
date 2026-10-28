import os
import hashlib

def h24(dane_bytes):
    return hashlib.sha256(dane_bytes).hexdigest()[:6]

def generuj_wariant(linie_bajty, v):
    wynik = bytearray()
    for i, linia in enumerate(linie_bajty):
        if linia.endswith(b'\n'):
            tresc = linia[:-1]
            if (v >> i) & 1:
                wynik.extend(tresc + b' \n')
            else:
                wynik.extend(tresc + b'\n')
        else:
            wynik.extend(linia)
    return bytes(wynik)

def uruchom_zadanie_3(orig_path="pliki-dla-studentow/oryginal.txt", mod_path="pliki-dla-studentow/zmieniony.txt"):
    if not os.path.exists(orig_path) or not os.path.exists(mod_path):
        print("Brak plików oryginal.txt i/lub zmieniony.txt")
        return

    with open(orig_path, "rb") as f:
        orig_lines = f.readlines()
    with open(mod_path, "rb") as f:
        mod_lines = f.readlines()

    slownik_oryginal = {}
    for v in range(8192):
        wariant_bytes = generuj_wariant(orig_lines, v)
        h = h24(wariant_bytes)
        if h not in slownik_oryginal:
            slownik_oryginal[h] = v

    h24_orig_v0 = h24(generuj_wariant(orig_lines, 0))

    pierwsza_para = None
    licznik_dopasowan_v0 = 0

    for v_mod in range(8192):
        wariant_mod_bytes = generuj_wariant(mod_lines, v_mod)
        h_mod = h24(wariant_mod_bytes)

        if pierwsza_para is None and h_mod in slownik_oryginal:
            v_orig = slownik_oryginal[h_mod]
            pierwsza_para = (v_orig, v_mod, h_mod)

        if h_mod == h24_orig_v0:
            licznik_dopasowan_v0 += 1

    if pierwsza_para:
        print(f"Para: ({pierwsza_para[0]}, {pierwsza_para[1]})")
        print(f"Wspólny skrót h24: {pierwsza_para[2]}")
    else:
        print("Nie znaleziono żadnej pary kolizyjnej.")

    print(f"Liczba wariantów zmienionego dokumentu z h24 równym h24: {licznik_dopasowan_v0}")

if __name__ == "__main__":
    uruchom_zadanie_3()