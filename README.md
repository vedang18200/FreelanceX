# FreelanceX - Deployment Guide

## 🔍 Where to Find Required Values

### 1. FREELANCEX_CONTRACT_ADDRESS

You need to **deploy your smart contract first**. Here's how:

#### Option A: Deploy via Brownie (Local)
```bash
# In your project directory
brownie console --network sepolia
>>> contract = FreelanceX.deploy({'from': accounts[0]})
>>> print(f"Contract Address: {contract.address}")
# Copy this address!
```

#### Option B: Deploy via Remix IDE
1. Go to [remix.ethereum.org](https://remix.ethereum.org)
2. Upload your `FreelanceX.sol` contract
3. Compile it
4. Switch to "Deploy & Run" tab
5. Connect MetaMask (Sepolia network)
6. Deploy contract
7. Copy the deployed contract address

#### Option C: Find Existing Deployment
Check your Brownie `build/deployments` folder:
```bash
# Look for deployed contracts
ls build/deployments/sepolia/
cat build/deployments/sepolia/FreelanceX.json
```

### 2. PRIVATE_KEY

Your wallet's private key for transactions:

#### From MetaMask:
1. Open MetaMask
2. Click on account menu (3 dots)
3. Account Details → Export Private Key
4. Enter password → Copy private key
5. **⚠️ NEVER share this publicly!**

#### From Brownie Accounts:
```bash
brownie accounts list
brownie accounts export <account_name>
# Enter password to see private key
```

#### Create New Test Account:
```bash
# Generate new account for testing
brownie accounts generate test_account
# Use this for testnet only!
```

### 3. STREAMLIT_SHARING

Simply set to `"true"` - this tells the app it's in hosted mode.

## 📋 Complete Setup Checklist

### Step 1: Deploy Contract
- [ ] Deploy FreelanceX.sol to Sepolia testnet
- [ ] Save contract address
- [ ] Verify deployment worked

### Step 2: Get Test ETH
- [ ] Visit [Sepolia Faucet](https://sepoliafaucet.com/)
- [ ] Enter your wallet address
- [ ] Get free Sepolia ETH

### Step 3: Set Streamlit Secrets
In Streamlit Cloud → App Settings → Secrets:
```toml
FREELANCEX_CONTRACT_ADDRESS = "0x1234...abcd"  # Your deployed contract
PRIVATE_KEY = "0xabcd1234..."                   # Your wallet private key
STREAMLIT_SHARING = "true"                      # Enable hosted mode
```

### Step 4: Test Locally First
```bash
# Create .env file with your values
echo 'FREELANCEX_CONTRACT_ADDRESS="0x..."' > .env
echo 'PRIVATE_KEY="0x..."' >> .env
echo 'STREAMLIT_SHARING="false"' >> .env

# Test locally
streamlit run streamlit_app.py
```

## 🚀 Quick Deploy Script

### v:\Block_chain\FreelanceX\deploy_sepolia.py

```python
from brownie import FreelanceX, accounts, network

def main():
    # Connect to Sepolia
    if network.show_active() != "sepolia":
        network.connect("sepolia")
    
    # Use your account
    account = accounts.load("your_account")  # or accounts[0] for default
    
    print(f"Deploying from: {account.address}")
    print(f"Balance: {account.balance() / 1e18:.4f} ETH")
    
    # Deploy contract
    contract = FreelanceX.deploy({'from': account})
    
    print(f"✅ Contract deployed!")
    print(f"📍 Address: {contract.address}")
    print(f"🔗 Etherscan: https://sepolia.etherscan.io/address/{contract.address}")
    print(f"\n📋 Add this to Streamlit secrets:")
    print(f'FREELANCEX_CONTRACT_ADDRESS = "{contract.address}"')

if __name__ == "__main__":
    main()
```

Run with: `brownie run deploy_sepolia.py --network sepolia`

## Hosting Options

### 1. Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set environment variables:
   - `FREELANCEX_CONTRACT_ADDRESS`: Your deployed contract address
   - `PRIVATE_KEY`: Your wallet private key (optional)

### 2. Heroku
```bash
heroku create your-freelancex-app
heroku config:set FREELANCEX_CONTRACT_ADDRESS=0x...
git push heroku main
```

### 3. Railway
1. Connect GitHub repo at [railway.app](https://railway.app)
2. Set environment variables in dashboard
3. Deploy automatically

### 4. Render
1. Connect GitHub repo at [render.com](https://render.com)
2. Choose "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

## Environment Variables
- `FREELANCEX_CONTRACT_ADDRESS`: Your smart contract address
- `PRIVATE_KEY`: Wallet private key (keep secure!)

## Local Development
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

# FreelanceX - Streamlit Cloud Deployment

## Quick Deploy to Streamlit Cloud

### 1. Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)
- Deployed smart contract on testnet/mainnet

### 2. Deploy Steps

1. **Fork/Clone this repo to your GitHub**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Click "New app"**
4. **Connect your GitHub repo**
5. **Set main file: `streamlit_app.py`**
6. **Configure secrets (see below)**
7. **Click Deploy!**

### 3. Required Secrets in Streamlit Cloud

Go to your app → Settings → Secrets, add:

```toml
FREELANCEX_CONTRACT_ADDRESS = "0xYourContractAddress"
STREAMLIT_SHARING = "true"
```

### 4. Deploy Smart Contract

For Sepolia testnet:
1. Get Sepolia ETH from faucet
2. Get Infura API key
3. Run deployment script:
```bash
pip install web3 python-dotenv
python deploy_contract.py
```

### 5. App Features
- ✅ Works on Sepolia, Mumbai, Mainnet
- ✅ Wallet connection via private key
- ✅ Post/take/complete jobs
- ✅ Real-time stats
- ✅ Transaction tracking

### 6. Environment Variables
- `FREELANCEX_CONTRACT_ADDRESS`: Your deployed contract
- `STREAMLIT_SHARING`: Set to "true" for hosted mode

## Local Development
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Live Demo
Visit your deployed app at: `https://yourapp.streamlit.app`

## 🔗 Useful Links

- **Sepolia Faucet**: https://sepoliafaucet.com/
- **Sepolia Explorer**: https://sepolia.etherscan.io/
- **Remix IDE**: https://remix.ethereum.org/
- **Streamlit Cloud**: https://share.streamlit.io/

## ⚠️ Security Notes

- **NEVER** commit private keys to Git
- Use `.gitignore` to exclude `.env` files
- Use testnet (Sepolia) for development
- Only use small amounts for testing

## 🆘 Troubleshooting

### "Contract not found"
- Verify contract is deployed: Check Etherscan
- Check contract address is correct
- Ensure you're on the right network

### "Insufficient funds"
- Get Sepolia ETH from faucet
- Check wallet balance
- Reduce gas fees

### "Invalid private key"
- Remove "0x" prefix if present
- Ensure key is 64 characters (hex)
- Test key with a small transaction first
