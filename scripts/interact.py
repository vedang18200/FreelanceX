from brownie import FreelanceX, accounts


def main():
    # Load first account from Brownie
    account = accounts[0]

    # Deploy contract
    contract = FreelanceX.deploy({'from': account})
    print("Deployed at:", contract.address)

    # Post a job
    tx = contract.postJob(
        "Build my portfolio website", 
        {'from': account, 'value': '1000000000000000000'}  # 1 ETH
    )
    tx.wait(1)
    print("Job Posted!")

    # Take the job using another account
    freelancer = accounts[1]
    tx = contract.takeJob(0, {'from': freelancer})
    tx.wait(1)
    print("Job Taken by:", freelancer)

    # Complete the job
    tx = contract.completeJob(0, {'from': account})
    tx.wait(1)
    print("Job Completed and Payment Sent!")
