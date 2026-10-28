import os
import hashlib

def sha256_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
        return hashlib.sha256(data).hexdigest()

def sprawdz_sumy_kontrolne(sha256sums_path="pliki-dla-studentow/SHA256SUMS.txt"):
    if not os.path.exists(sha256sums_path):
        print(f"Brak pliku {sha256sums_path} w podanym katalogu.")
        return

    base_dir = os.path.dirname(sha256sums_path) or "."

    with open(sha256sums_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split("  ", 1)
            if len(parts) < 2:
                continue

            expected_hash, rel_path = parts
            full_path = os.path.join(base_dir, rel_path)

            if not os.path.exists(full_path):
                status = "BRAK"
            else:
                try:
                    actual_hash = sha256_file(full_path)
                    status = "OK" if actual_hash.lower() == expected_hash.lower() else "BŁĄD"
                except Exception:
                    status = "BŁĄD"

            print(f"{rel_path}: {status}")

def porownaj_bity_tekstow():
    t1 = b"Ala ma kota."
    t2 = b"Ola ma kota."

    h1_bytes = hashlib.sha256(t1).digest()
    h2_bytes = hashlib.sha256(t2).digest()

    diff_bits = 0
    for b1, b2 in zip(h1_bytes, h2_bytes):
        xor_result = b1 ^ b2
        diff_bits += bin(xor_result).count('1')

    print(f"Ala ma kota. -> {hashlib.sha256(t1).hexdigest()}")
    print(f"Ola ma kota. -> {hashlib.sha256(t2).hexdigest()}")
    print(f"Liczba różniących się bitów: {diff_bits} / 256")

if __name__ == "__main__":
    sprawdz_sumy_kontrolne()
    porownaj_bity_tekstow()