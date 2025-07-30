from brownie import FreelanceX, accounts

def main():
    account = accounts[0]
    print(f"Deploying from: {account}")
    FreelanceX.deploy({'from': account})
