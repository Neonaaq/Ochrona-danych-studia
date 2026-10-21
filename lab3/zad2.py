from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def szyfruj_odszyfruj(dane):
    haslo = "SmacznejKawusi"
    sol = get_random_bytes(16)
    klucz = PBKDF2(haslo.encode('utf-8'), sol, dkLen=32, count=200000)

    iv = get_random_bytes(16)

    cipher = AES.new(klucz, AES.MODE_CBC, iv)

    zaszyfrowane_dane = cipher.encrypt(pad(dane, AES.block_size))
    print(f"Długość kryptogramu: {len(zaszyfrowane_dane)} bajtów")

    decipher = AES.new(klucz, AES.MODE_CBC, iv)
    odszyfrowane_dane = unpad(decipher.decrypt(zaszyfrowane_dane), AES.block_size)

    if odszyfrowane_dane == dane:
        print("Dane odszyfrowane poprawnie.\n")

    return sol, iv, zaszyfrowane_dane

dane1 = b""
dane2 = b"0123456789ABCDEF"
with open("wiadomosc.txt", 'rb') as file:
    dane3 = file.read()

sol1, iv1, kryptogram1 = szyfruj_odszyfruj(dane1)
sol2, iv2, kryptogram2 = szyfruj_odszyfruj(dane2)
sol3, iv3, kryptogram3 = szyfruj_odszyfruj(dane3)
sol4, iv4, kryptogram4 = szyfruj_odszyfruj(dane3)

if kryptogram3 == kryptogram4:
    print("Kryptogramy zaszyfrowane tymi samymi danymi, ale z inną solą i iv są takie same.")
else:
    print("Kryptogramy zaszyfrowane tymi samymi danymi, ale z inną solą i iv są inne.")

