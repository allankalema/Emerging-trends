import hashlib
from Crypto.Hash import keccak  # Requires pycryptodome package

def hash_sha256(message):
    return hashlib.sha256(message.encode()).hexdigest()

def hash_sha3_256(message):
    return hashlib.sha3_256(message.encode()).hexdigest()

def hash_blake2s(message):
    return hashlib.blake2s(message.encode()).hexdigest()

def hash_keccak256(message):
    return keccak.new(data=message.encode(), digest_bits=256).hexdigest()

def main():
    message = input("Enter a message to hash: ")
    
    print("\nHash digests using different algorithms:")
    print(f"SHA-256:     {hash_sha256(message)}")
    print(f"SHA3-256:    {hash_sha3_256(message)}")
    print(f"BLAKE2s:     {hash_blake2s(message)}")
    print(f"Keccak-256:  {hash_keccak256(message)}")

if __name__ == "__main__":
    main()


# Blockchain is a decentralized, secure, and tamper-proof digital ledger technology. It records transactions in blocks, with each block containing a unique hash and the hash of the previous block, forming an unbreakable chain. This ensures transparency, security, and immutability, making it ideal for financial systems, cryptocurrencies, supply chains, and more. Blockchain operates without a central authority, relying on consensus mechanisms like Proof-of-Work or Proof-of-Stake to validate transactions. Any attempt to alter a block changes its hash, invalidating all subsequent blocks. This cryptographic security makes blockchain resistant to fraud and cyberattacks, revolutionizing trust in digital transactions.