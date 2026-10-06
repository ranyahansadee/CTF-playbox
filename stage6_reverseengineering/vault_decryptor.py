import sys

XOR_KEY = b"AegisRogueRE2026"
MASTER_PASSWORD = "R3v3rse_Th1s!"

def xor(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def main():
    password = input("Enter master decryption password: ")
    if password != MASTER_PASSWORD:
        print("Access denied.")
        sys.exit(1)
    try:
        with open("vault.enc", "rb") as f:
            enc = f.read()
    except FileNotFoundError:
        print("vault.enc not found in current directory.")
        sys.exit(1)
    dec = xor(enc, XOR_KEY)
    print("Vault unlocked:")
    print(dec.decode())

if __name__ == "__main__":
    main()
