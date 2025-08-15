# FreelanceX

A minimal decentralized freelancing platform built with **Solidity** smart contracts and a **Python/Streamlit** frontend. Post gigs, hire freelancers, and manage job milestones with on-chain transparency.

> Tech stack: Solidity (contracts), Python + Streamlit (UI), web3.py (chain interface).  
> Repo layout includes `contracts/`, `scripts/`, `streamlit_app.py`, and `requirements.txt`. :contentReference[oaicite:0]{index=0}

---

## ✨ Features

- Create & browse freelance jobs
- Client ↔️ Freelancer workflows
- On-chain state for jobs/milestones
- Basic escrow flow (deposit → delivery → release/refund)
- Simple, clean Streamlit UI

> Languages in this repo are primarily Python and Solidity. :contentReference[oaicite:1]{index=1}

---

## 📦 Project Structure

FreelanceX/
├─ contracts/ # Solidity smart contracts
├─ scripts/ # Helper scripts (deploy/interact)
├─ streamlit_app.py # Streamlit frontend
├─ requirements.txt # Python dependencies
└─ README.md

> Directories and key files confirmed in the repository listing. :contentReference[oaicite:2]{index=2}

---

## 🚀 Quick Start (Local)

### 1) Prereqs
- Python 3.10+  
- Node.js (only if you use Hardhat)  
- A local Ethereum RPC (Anvil, Hardhat, or Ganache)

### 2) Install Python deps
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
3) Start a local chain
```

Hardhat
```
npm i -g hardhat
npx hardhat node
```

Ganache
```
npm i -g ganache
ganache
```
4) Deploy contracts

Use the scripts in scripts/ (names may vary). Common patterns:

# Example: Python deploy (web3.py)
```
python scripts/deploy.py
# or
python scripts/deploy_contracts.py
```

Capture the printed contract address (e.g., FreelanceX/JobManager) for the frontend config.

If your deploy script name differs, check the scripts/ folder and adjust accordingly. 
GitHub

5) Configure environment

Create a .env in the project root:

# RPC and account (dev only; use test keys)
```
WEB3_PROVIDER_URI=http://127.0.0.1:8545
PRIVATE_KEY=0xYOUR_LOCAL_DEV_PRIVATE_KEY
```
# Contract linkage for the UI
```
CONTRACT_ADDRESS=0xDeployedContractAddress
```
# Either paste ABI JSON directly or point to a file path
```
CONTRACT_ABI_PATH=./contracts/build/FreelanceX.json
```
# Streamlit (optional)
```
STREAMLIT_SERVER_PORT=8501
```
Never commit real private keys. Use local/test keys only.

6) Run the app
```
streamlit run streamlit_app.py
```
🧭 How It Works

Client creates a job with budget → funds escrow.

Freelancer applies/accepts → starts work.

Milestones can be marked complete.

Client releases escrow (or disputes → refund path, if implemented).

All critical state is on-chain via the Solidity contracts in contracts/.

🔧 Development Notes

Prefer running against a local chain first (Anvil/Hardhat/Ganache).

If targeting a public testnet (e.g., Sepolia/Amoy), set WEB3_PROVIDER_URI and fund your dev account with test ETH/MATIC.

After each re-deploy, update CONTRACT_ADDRESS and (if ABI changed) CONTRACT_ABI_PATH for the Streamlit app.

Typical Python modules used here: web3, python-dotenv, streamlit (see requirements.txt). 
GitHub

🧪 Testing

Add unit tests for contracts (Foundry/Hardhat) and integration tests for Python/web3 flows.

Example (Foundry):
```
forge test
```

Example (Hardhat):
```
npx hardhat test
```
🔐 Security

Do not use mainnet with un-audited contracts or real funds.

Keep secrets in .env and out of version control.

Consider multisig for admin roles and timelocks for upgrades (if you add them later).

📄 License

MIT (recommended). Create a LICENSE file or update this section with your chosen license.

🙌 Contributing

PRs and issues are welcome:

Keep PRs small and focused.

Add tests for any contract or logic change.

Update this README when you change setup steps.

🗺️ Roadmap (suggested)

Role-based dashboards (Client/Freelancer)

Dispute resolution module

Milestone-based partial releases

Reputation/ratings on-chain or hybrid

IPFS/Arweave for deliverables metadata

Email/Telegram notifications via webhooks

💬 Support

Open an issue on GitHub with:

Environment (OS, Python version)

Chain (local/testnet), steps to reproduce

Logs/screenshots


If you want, I can also add a **badges row**, a **diagram**, or wire up a ready-to-use `deploy.py` that matches your current contracts—just say the word.
::contentReference[oaicite:7]{index=7}
