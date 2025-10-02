# FreelanceX - Deployment Guide

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
