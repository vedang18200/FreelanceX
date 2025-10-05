import json

# Read the compiled contract
with open('build/contracts/FreelanceX.json', 'r') as f:
    contract_data = json.load(f)

# Extract ABI
abi = contract_data['abi']

# Save to file for easy copying
with open('contract_abi.json', 'w') as f:
    json.dump(abi, f, indent=2)

print("ABI extracted to contract_abi.json")
print("Copy this ABI to your Streamlit Cloud app!")
