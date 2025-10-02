from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Contract bytecode and ABI (from your compiled contract)
CONTRACT_BYTECODE = "0x608060405234801561001057600080fd5b50..."  # Your contract bytecode
CONTRACT_ABI = [
    {"inputs": [{"internalType": "string", "name": "_description", "type": "string"}], "name": "postJob", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_jobId", "type": "uint256"}], "name": "takeJob", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_jobId", "type": "uint256"}], "name": "completeJob", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "getJobCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_jobId", "type": "uint256"}], "name": "getJob", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "string", "name": "", "type": "string"}, {"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}
]

def deploy_to_sepolia():
    # Connect to Sepolia
    w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{os.getenv('INFURA_API_KEY')}"))

    if not w3.is_connected():
        print("❌ Failed to connect to Sepolia")
        return None

    print("✅ Connected to Sepolia")

    # Setup account
    private_key = os.getenv("PRIVATE_KEY")
    account = w3.eth.account.from_key(private_key)

    print(f"Deploying from: {account.address}")

    # Create contract
    contract = w3.eth.contract(abi=CONTRACT_ABI, bytecode=CONTRACT_BYTECODE)

    # Build deployment transaction
    tx = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
    })

    # Sign and send
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"Transaction sent: {tx_hash.hex()}")

    # Wait for confirmation
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if tx_receipt.status == 1:
        print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")
        print(f"Set this as FREELANCEX_CONTRACT_ADDRESS: {tx_receipt.contractAddress}")
        return tx_receipt.contractAddress
    else:
        print("❌ Deployment failed")
        return None

if __name__ == "__main__":
    deploy_to_sepolia()
