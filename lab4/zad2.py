import os
import hashlib
import hmac
import secrets

def pbkdf2_hash(password_str, salt_bytes, iterations):
    pwd_bytes = password_str.encode('utf-8')
    return hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, iterations, dklen=32)

def wczytaj_baze_hasel(filepath="pliki-dla-studentow/hasla.txt"):
    baza = {}
    if not os.path.exists(filepath):
        print(f"Brak pliku {filepath}.")
        return baza

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) == 4:
                login, iters, salt_hex, hash_hex = parts
                baza[login] = {
                    'iters': int(iters),
                    'salt': bytes.fromhex(salt_hex),
                    'hash': bytes.fromhex(hash_hex)
                }
    return baza

def weryfikuj(login, haslo, baza):
    if login not in baza:
        return False

    rec = baza[login]
    calculated_hash = pbkdf2_hash(haslo, rec['salt'], rec['iters'])

    return hmac.compare_digest(calculated_hash, rec['hash'])

def dodaj(login, haslo, baza):
    salt = secrets.token_bytes(16)
    iters = 600000
    hash_val = pbkdf2_hash(haslo, salt, iters)

    baza[login] = {
        'iters': iters,
        'salt': salt,
        'hash': hash_val
    }
    return salt, hash_val

if __name__ == "__main__":
    baza = wczytaj_baze_hasel()

    t1 = weryfikuj("anna", "Kasztan-2026", baza)
    t2 = weryfikuj("anna", "kasztan-2026", baza)
    t3 = weryfikuj("piotr", "Żółw na łące", baza)
    t4 = weryfikuj("kasia", "Kasztan-2026", baza)

    print(f"1. anna (Kasztan-2026): {t1}")
    print(f"2. anna (kasztan-2026): {t2}")
    print(f"3. piotr (Żółw na łące): {t3}")
    print(f"4. kasia (Kasztan-2026): {t4}")

    haslo_testowe = "test"
    salt1, hash1 = dodaj("test1", haslo_testowe, baza)
    salt2, hash2 = dodaj("test2", haslo_testowe, baza)

    print(f"Czy sole test1 i test2 są identyczne?: {salt1 == salt2}")
    print(f"Czy skróty test1 i test2 są identyczne?: {hash1 == hash2}")

    weryfikacja_test1 = weryfikuj("test1", haslo_testowe, baza)
    weryfikacja_test2 = weryfikuj("test2", haslo_testowe, baza)
    print(f"Weryfikacja konta test1: {weryfikacja_test1}")
    print(f"Weryfikacja konta test2: {weryfikacja_test2}")