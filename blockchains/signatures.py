import hashlib
import ecdsa
import binascii

def generate_keys():
    """Generate a new ECDSA private and public key pair."""
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    
    # Convert keys to hex for easy input/output
    private_hex = binascii.hexlify(private_key.to_string()).decode()
    public_hex = binascii.hexlify(public_key.to_string()).decode()
    
    return private_key, public_key, private_hex, public_hex

def sign_message(private_key, message):
    """Sign a message using the private key."""
    message_hash = hashlib.sha256(message.encode()).digest()
    signature = private_key.sign(message_hash)
    
    # Convert signature to hex for easy input/output
    return binascii.hexlify(signature).decode()

def verify_signature(public_hex, message, signature_hex):
    """Verify a digital signature using the public key."""
    try:
        # Convert hex values back to original format
        public_bytes = binascii.unhexlify(public_hex)
        public_key = ecdsa.VerifyingKey.from_string(public_bytes, curve=ecdsa.SECP256k1)
        signature = binascii.unhexlify(signature_hex)
        
        # Hash the message and verify the signature
        message_hash = hashlib.sha256(message.encode()).digest()
        return public_key.verify(signature, message_hash)
    except (ecdsa.BadSignatureError, ValueError):
        return False

def main():
    print("\n🔑 **Step 1: Key Generation** 🔑")
    private_key, public_key, private_hex, public_hex = generate_keys()
    print(f"\nPrivate Key (Keep Secret!):\n{private_hex}")
    print(f"\nPublic Key (Share this for verification):\n{public_hex}")

    input("\nPress Enter to continue to message signing...")

    print("\n🖊 **Step 2: Signing a Message** 🖊")
    message = input("\nEnter the message you want to sign: ")
    signature_hex = sign_message(private_key, message)
    print(f"\nGenerated Signature:\n{signature_hex}")

    input("\nPress Enter to continue to verification...")

    print("\n✅ **Step 3: Verifying the Signature** ✅")
    pub_key_input = input("\nEnter the public key for verification: ")
    sig_input = input("\nEnter the signature: ")
    msg_input = input("\nEnter the original message: ")

    is_valid = verify_signature(pub_key_input, msg_input, sig_input)
    print("\nVerification Result:", "✅ Valid Signature!" if is_valid else "❌ Invalid Signature!")

if __name__ == "__main__":
    main()
