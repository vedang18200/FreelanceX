#!/usr/bin/env python3
"""
FreelanceX Deployment Script
"""

from brownie import FreelanceX, accounts, network

def main():
    print("🚀 FreelanceX Deployment Starting...")
    print("=" * 50)
    
    # Get deployment account
    account = accounts[0]
    print(f"📝 Deploying from account: {account}")
    print(f"💰 Account balance: {account.balance() / 10**18:.4f} ETH")
    print(f"🌐 Network: {network.show_active()}")
    print()
    
    # Deploy the contract
    print("🔄 Deploying FreelanceX contract...")
    try:
        freelance_x = FreelanceX.deploy({'from': account})
        
        print("✅ FreelanceX deployed successfully!")
        print(f"📍 Contract address: {freelance_x.address}")
        print(f"⛽ Gas used: {freelance_x.tx.gas_used:,}")
        print(f"💸 Gas price: {freelance_x.tx.gas_price / 10**9:.2f} Gwei")
        print(f"🧾 Transaction hash: {freelance_x.tx.txid}")
        print()
        
        # Test basic functionality
        print("🧪 Testing basic functionality...")
        
        # Test job posting
        print("📝 Testing job posting...")
        tx = freelance_x.postJob("Test Job Description", {'from': account, 'value': 1000000000000000000})  # 1 ETH
        tx.wait(1)
        print("✅ Job posted successfully!")
        
        # Test job retrieval
        print("🔍 Testing job retrieval...")
        job_count = freelance_x.getJobCount()
        print(f"📊 Total jobs: {job_count}")
        
        if job_count > 0:
            job = freelance_x.getJob(0)
            print(f"🏷️  Job 0 details:")
            print(f"   ID: {job[0]}")
            print(f"   Client: {job[1]}")
            print(f"   Description: {job[3]}")
            print(f"   Budget: {job[4] / 10**18} ETH")
            print(f"   Status: {['Open', 'InProgress', 'Completed'][job[5]]}")
        
        print("✅ All tests passed!")
        print()
        print("🎉 Deployment completed successfully!")
        print(f"🔗 You can now interact with the contract at: {freelance_x.address}")
        
        return freelance_x
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        raise

def deploy():
    """Alternative entry point for programmatic deployment"""
    return main()

if __name__ == "__main__":
    main()