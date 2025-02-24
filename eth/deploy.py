from web3 import Web3
import json

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if we're connected to Ganache
if not web3.is_connected():
    print("Failed to connect to Ganache.")
    exit(1)

print("Connected to Ganache.")

# Load the compiled contract
with open("StudentRecords.json", "r") as file:
    contract_data = json.load(file)

# Extract ABI and bytecode
abi = contract_data.get("abi")
bytecode = contract_data.get("bytecode")

if abi is None or bytecode is None:
    print("ABI or Bytecode not found in the compiled contract.")
    exit(1)

# Set up account and gas
account = web3.eth.accounts[0]
web3.eth.default_account = account

# Check balance of the account to ensure there are enough funds to deploy
balance = web3.eth.get_balance(account)
print(f"Account balance: {web3.from_wei(balance, 'ether')} ETH")

# Set gas and gas price
gas_price = web3.to_wei('20', 'gwei')
gas_limit = 4000000  # Adjust the gas limit as needed

try:
    # Deploy contract
    StudentRecords = web3.eth.contract(abi=abi, bytecode=bytecode)
    transaction = StudentRecords.constructor().build_transaction({
        'chainId': 1337,  # Ganache default chain ID
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': web3.eth.get_transaction_count(account),
    })

    # Send the transaction directly (Web3 will sign it internally)
    tx_hash = web3.eth.send_transaction(transaction)

    # Wait for the transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    print(f"Contract deployed at: {contract_address}")

    # Save the contract address to a file for later use
    with open("contract_address.txt", "w") as file:
        file.write(contract_address)

except Exception as e:
    print(f"Error deploying contract: {e}")
