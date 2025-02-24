from django.shortcuts import render
from .blockchain import Blockchain
from django.core.serializers import serialize
import json
from .blockchain import Block, Blockchain
from .hashes import hash_sha256, hash_sha3_256, hash_blake2s, hash_keccak256
from .signatures import generate_keys, sign_message, verify_signature

# Blockchain View
# Blockchain View
def blockchain_view(request):
    # Check if blockchain data is in session, otherwise initialize it
    blockchain_data = request.session.get('blockchain_data', None)
    if blockchain_data is None:
        blockchain = Blockchain(difficulty=4)
        request.session['blockchain_data'] = [block.__dict__ for block in blockchain.chain]  # Save the chain data
    else:
        blockchain = Blockchain(difficulty=4)
        blockchain.chain = [Block(index=block['index'], previous_hash=block['previous_hash'], data=block['data'], difficulty=block['difficulty']) for block in blockchain_data]  # Rebuild the blockchain from session data

    # Handle form submission for adding a block
    if request.method == 'POST':
        data = request.POST.get('data')
        blockchain.add_block(data)
        # Store the updated blockchain in session as a list of dicts
        request.session['blockchain_data'] = [block.__dict__ for block in blockchain.chain]

    # Prepare data to render in the template
    chain_data = [{
        'index': block.index,
        'timestamp': block.timestamp,
        'data': block.data,
        'nonce': block.nonce,
        'previous_hash': block.previous_hash,
        'hash': block.hash
    } for block in blockchain.chain]

    return render(request, 'blockchain/blockchain_page.html', {'chain': chain_data})

# Hashing View
def hashing_view(request):
    sha256 = sha3_256 = blake2s = keccak_256 = None
    if request.method == 'POST':
        message = request.POST.get('message')
        sha256 = hash_sha256(message)
        sha3_256 = hash_sha3_256(message)
        blake2s = hash_blake2s(message)
        keccak_256 = hash_keccak256(message)

    return render(request, 'blockchain/hashing_page.html', {
        'sha256': sha256,
        'sha3_256': sha3_256,
        'blake2s': blake2s,
        'keccak_256': keccak_256
    })

def signature_view(request):
    signature = verification = None
    private_key = public_key = None
    message = None  # Define message variable

    if request.method == 'POST':
        if 'message' in request.POST:
            # Handle message signing logic when the "Sign Message" form is submitted
            message = request.POST.get('message')
            if message:  # Ensure message is not empty
                private_key, public_key, private_hex, public_hex = generate_keys()
                signature = sign_message(private_key, message)

                # Pass keys and message to the context so they can be rendered in the template
                private_key = private_hex
                public_key = public_hex
            else:
                verification = "❌ Please provide a message to sign."
        
        elif 'verify_public_key' in request.POST:
            # Handle signature verification when the "Verify Signature" form is submitted
            pub_key_input = request.POST.get('verify_public_key')
            msg_input = request.POST.get('verify_message')
            sig_input = request.POST.get('verify_signature')
            
            if msg_input and sig_input and pub_key_input:
                verification = "✅ Valid Signature!" if verify_signature(pub_key_input, msg_input, sig_input) else "❌ Invalid Signature!"
            else:
                verification = "❌ Please provide a message, signature, and public key for verification."

    return render(request, 'blockchain/signature_page.html', {
        'signature': signature,
        'verification': verification,
        'private_key': private_key,
        'public_key': public_key,
        'message': message  # Pass message to context
    })
