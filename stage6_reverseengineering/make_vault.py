XOR_KEY = b"AegisRogueRE2026"
FLAG = b"ROGUE{byt3c0d3_n3v3r_l13s}"

def xor(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

with open("vault.enc", "wb") as f:
    f.write(xor(FLAG, XOR_KEY))

print("vault.enc created")

