from django.shortcuts import render, redirect
from web3 import Web3
import json
import os

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load the contract address
contract_address = None
if os.path.exists("eth/contract_address.txt"):
    with open("eth/contract_address.txt", "r") as file:
        contract_address = file.read().strip()
else:
    print("Contract address file not found. Please deploy the contract first.")

# Load the contract ABI
if contract_address:
    with open("eth/StudentRecords.json", "r") as file:
        contract_data = json.load(file)
        abi = contract_data["abi"]

    # Create contract instance
    contract = web3.eth.contract(address=contract_address, abi=abi)
else:
    contract = None

def wallet_balance(request):
    if not contract:
        return render(request, "eth/error.html", {"message": "Contract not deployed. Please deploy the contract first."})

    account = web3.eth.accounts[0]  # First account in Ganache
    balance = web3.eth.get_balance(account)
    eth_balance = web3.from_wei(balance, 'ether')  # Use from_wei() instead of fromWei()

    # Fetch gas price from Ganache
    gas_price = web3.eth.gas_price
    gas_price_in_ether = web3.from_wei(gas_price, 'ether')  # Use from_wei() instead of fromWei()

    return render(request, "eth/wallet_balance.html", {
        "balance": eth_balance,
        "account": account,
        "gas_price": gas_price_in_ether,
    })

def register_student(request):
    if not contract:
        return render(request, "eth/error.html", {"message": "Contract not deployed. Please deploy the contract first."})

    if request.method == "POST":
        name = request.POST.get("name")
        student_id = int(request.POST.get("student_id"))
        try:
            tx_hash = contract.functions.registerStudent(name, student_id).transact({
                'from': web3.eth.accounts[0],
            })
            web3.eth.wait_for_transaction_receipt(tx_hash)
            return redirect("view_student")
        except Exception as e:
            print(f"Error: {e}")
    return render(request, "eth/register_student.html")

def view_student(request):
    if not contract:
        return render(request, "eth/error.html", {"message": "Contract not deployed. Please deploy the contract first."})

    error = None
    name = None
    student_id = None
    student_address = None
    all_students = []

    if request.method == "POST":
        student_address = request.POST.get("student_address")
        if not student_address.startswith("0x") or len(student_address) != 42:
            error = "Invalid Ethereum address. Address must start with '0x' and be 42 characters long."
        else:
            try:
                name, student_id = contract.functions.getStudent(student_address).call()
            except Exception as e:
                error = f"Error retrieving student record: {e}"

    # Retrieve all student addresses
    try:
        student_addresses = contract.functions.getAllStudents().call()
        for address in student_addresses:
            name, student_id = contract.functions.getStudent(address).call()
            all_students.append({
                "name": name,
                "student_id": student_id,
                "address": address,
            })
    except Exception as e:
        error = f"Error retrieving all students: {e}"

    return render(request, "eth/view_student.html", {
        "name": name,
        "student_id": student_id,
        "student_address": student_address,
        "all_students": all_students,
        "error": error,
    })