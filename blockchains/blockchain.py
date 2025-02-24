import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, data, difficulty=4):
        self.index = index
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Readable timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Proof of Work (incremented until hash meets difficulty)
        self.difficulty = difficulty  # Number of leading zeros required
        self.hash = self.mine_block()  # Generate hash via PoW

    def to_dict(self):
        """Serialize the block to a dictionary."""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'nonce': self.nonce,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

    def calculate_hash(self):
        """Generate the hash based on block contents."""
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        """Perform Proof of Work: find a hash with the required number of leading zeros."""
        prefix = "0" * self.difficulty  # Define difficulty (e.g., "0000")
        while True:
            new_hash = self.calculate_hash()
            if new_hash.startswith(prefix):
                return new_hash
            self.nonce += 1  # Increment nonce to change the hash


class Blockchain:
    def __init__(self, difficulty=4):
        """Initialize blockchain with difficulty setting."""
        self.difficulty = difficulty  # Set difficulty level first!
        self.chain = [self.create_genesis_block()]  # Now create the first block

    def create_genesis_block(self):
        """Create the first block manually."""
        return Block(0, "0", "Genesis Block", self.difficulty)

    def add_block(self, data):
        """Add a new block with Proof of Work."""
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, data, self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Verify blockchain integrity."""
        for i in range(1, len(self.chain)):  # Skip Genesis Block
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Recalculate hash & verify
            if current_block.hash != current_block.calculate_hash():
                print(f"🚨 Block {current_block.index} has been tampered with!")
                return False

            # Ensure chain is linked properly
            if current_block.previous_hash != previous_block.hash:
                print(f"🔗 Block {current_block.index} is not properly linked!")
                return False

        print("✅ Blockchain is valid!")
        return True

    def print_chain(self):
        """Print blockchain for visualization."""
        for block in self.chain:
            print(f"\n🔗 Block {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Nonce: {block.nonce}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
