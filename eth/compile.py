import json
from solcx import compile_standard, install_solc

# Install Solidity compiler version
install_solc("0.8.0")

# Read the Solidity contract
with open("StudentRecords.sol", "r") as file:
    student_contract = file.read()

# Compile the contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"StudentRecords.sol": {"content": student_contract}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode", "evm.bytecode.sourceMap"],
                }
            }
        },
    },
    solc_version="0.8.0",
)

# Extract the contract name dynamically
contract_name = list(compiled_sol["contracts"]["StudentRecords.sol"].keys())[0]

# Extract ABI & Bytecode
abi = compiled_sol["contracts"]["StudentRecords.sol"][contract_name]["abi"]
bytecode = compiled_sol["contracts"]["StudentRecords.sol"][contract_name]["evm"]["bytecode"]["object"]

# Save compiled contract
compiled_contract = {"abi": abi, "bytecode": bytecode}

with open("StudentRecords.json", "w") as file:
    json.dump(compiled_contract, file, indent=4)

print("Contract compiled successfully! JSON saved as StudentRecords.json")
