import streamlit as st
import os
import sys
import json
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set working directory to script directory (safe for both CLI and Streamlit)
if "__file__" in globals():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="FreelanceX", layout="wide")

# Debug Info
st.sidebar.header("🔧 Debug Info")
st.sidebar.write(f"**Current Directory:** {os.getcwd()}")
st.sidebar.write(f"**Python Path:** {sys.executable}")

# Check if we're in hosted environment
is_hosted = os.getenv("STREAMLIT_SHARING") or os.getenv("HEROKU") or os.getenv("RAILWAY") or os.getenv("RENDER")
st.sidebar.write(f"**Hosted Environment:** {bool(is_hosted)}")

# Contract ABI for hosted environments
CONTRACT_ABI = [
    {"inputs": [{"internalType": "string", "name": "_description", "type": "string"}], "name": "postJob", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_jobId", "type": "uint256"}], "name": "takeJob", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_jobId", "type": "uint256"}], "name": "completeJob", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "getJobCount", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "_jobId", "type": "uint256"}], "name": "getJob", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "string", "name": "", "type": "string"}, {"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}
]

# Import contract
FreelanceX = None
accounts = None
network = None

if not is_hosted:
    try:
        from brownie import FreelanceX, accounts, network
        st.sidebar.success("✅ Brownie import successful!")
    except ImportError:
        st.sidebar.warning("⚠️ Brownie not available, using Web3 mode")
        is_hosted = True  # Force Web3 mode if Brownie fails
else:
    st.sidebar.info("🌐 Using Web3 for hosted environment")

def setup_web3_connection():
    """Setup Web3 connection for hosted environments"""
    try:
        network_options = {
            "Sepolia Testnet": {
                "rpc": "https://sepolia.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
                "chain_id": 11155111
            },
            "Polygon Mumbai": {
                "rpc": "https://rpc-mumbai.maticvigil.com",
                "chain_id": 80001
            },
            "Ethereum Mainnet": {
                "rpc": "https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
                "chain_id": 1
            }
        }

        selected_network = st.sidebar.selectbox("🌐 Select Network", list(network_options.keys()))

        if selected_network:
            network_config = network_options[selected_network]
            w3 = Web3(Web3.HTTPProvider(network_config["rpc"]))

            if w3.is_connected():
                st.sidebar.success(f"✅ Connected to {selected_network}")
                return w3, network_config["chain_id"]
            else:
                st.sidebar.error("❌ Failed to connect to network")
                return None, None

        return None, None
    except Exception as e:
        st.error(f"Failed to connect to public network: {e}")
        return None, None

def setup_web3_account(w3):
    """Setup account for Web3 connection"""
    st.sidebar.header("👛 Wallet Connection")

    private_key = st.sidebar.text_input("🔐 Private Key", type="password", help="Your wallet private key")

    if private_key:
        try:
            account = w3.eth.account.from_key(private_key)
            balance = w3.eth.get_balance(account.address)
            st.sidebar.success("✅ Wallet connected")
            st.sidebar.write(f"**Address:** {account.address}")
            st.sidebar.write(f"**Balance:** {Web3.from_wei(balance, 'ether'):.4f} ETH")
            return account
        except Exception as e:
            st.sidebar.error(f"Invalid private key: {e}")
            return None
    return None

def connect():
    """Connect to network - Brownie version"""
    try:
        if network.show_active() != "development":
            network.connect("development")
        return accounts
    except Exception as e:
        st.error(f"⚠️ Network error: {e}")
        return []

def get_or_deploy_contract(account):
    """Get deployed contract or help user deploy to public network - Brownie version"""
    contract_address = os.getenv("FREELANCEX_CONTRACT_ADDRESS")

    if contract_address:
        try:
            contract = FreelanceX.at(contract_address)
            st.success(f"✅ Connected to contract at {contract_address}")
            return contract
        except Exception as e:
            st.error(f"Failed to connect to contract at {contract_address}: {e}")

    try:
        if len(FreelanceX) > 0:
            contract = FreelanceX[-1]
            st.success(f"✅ Connected to contract at {contract.address}")
            return contract
    except:
        pass

    st.warning("⚠️ No deployed contract found on this network.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Deploy New Contract"):
            try:
                with st.spinner("Deploying contract..."):
                    contract = FreelanceX.deploy({'from': account})
                    st.success(f"✅ Contract deployed at {contract.address}")
                    return contract
            except Exception as e:
                st.error(f"Deployment failed: {e}")

    with col2:
        manual_address = st.text_input("📍 Enter Contract Address")
        if manual_address and st.button("🔗 Connect"):
            try:
                contract = FreelanceX.at(manual_address)
                st.success(f"✅ Connected to contract at {manual_address}")
                return contract
            except Exception as e:
                st.error(f"Failed to connect: {e}")

    return None

# Main application logic
if is_hosted:
    # Use Web3 for hosted environments
    w3, chain_id = setup_web3_connection()
    if not w3:
        st.error("❌ Failed to connect to network")
        st.stop()

    account = setup_web3_account(w3)
    if not account:
        st.error("❌ Please connect your wallet")
        st.stop()

    # Get contract
    contract_address = os.getenv("FREELANCEX_CONTRACT_ADDRESS")
    if not contract_address:
        st.error("❌ Contract address not found. Please set FREELANCEX_CONTRACT_ADDRESS environment variable.")
        st.info("Deploy your contract and set the address in your hosting platform's environment variables.")
        st.stop()

    try:
        contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
        st.success(f"✅ Connected to contract at {contract_address}")
    except Exception as e:
        st.error(f"Failed to connect to contract: {e}")
        st.stop()
else:
    # Local development with Brownie
    accounts_list = connect()
    if not accounts_list:
        st.error("❌ Failed to connect wallet. Please check your setup.")
        st.stop()

    # Sidebar account info for Brownie
    with st.sidebar:
        st.header("🔗 Connection Info")
        try:
            st.write(f"**Network:** {network.show_active()}")
            account_addresses = [acct.address for acct in accounts_list]
            selected_address = st.selectbox("👛 Select Wallet", account_addresses)

            # Find the actual account object
            account = next(acct for acct in accounts_list if acct.address == selected_address)

            st.write(f"**Address:** {selected_address}")
            balance = account.balance() / 10**18
            st.write(f"**Balance:** {balance:.4f} ETH")

            if balance < 0.01:
                st.warning("⚠️ Low balance! You may need more ETH for transactions.")

        except Exception as e:
            st.error(f"⚠️ Account error: {e}")
            st.stop()

    # Get or deploy contract
    contract = get_or_deploy_contract(account)
    if not contract:
        st.stop()

st.title("🧑‍💻 FreelanceX - Decentralized Freelancing Platform")

# Main layout
col1, col2 = st.columns([2, 1])

# LEFT: Post and View Jobs
with col1:
    st.markdown("---")
    st.header("📢 Post a Job")
    with st.form("post_job"):
        desc = st.text_area("📝 Job Description", placeholder="Describe your job...")
        eth = st.number_input("💰 Budget (ETH)", min_value=0.001, value=0.1, step=0.001, format="%.3f")
        if st.form_submit_button("📤 Post Job"):
            if not desc.strip():
                st.error("❌ Description cannot be empty.")
            else:
                try:
                    wei = Web3.to_wei(eth, 'ether')

                    if is_hosted:
                        # Web3 transaction
                        balance = w3.eth.get_balance(account.address)
                        if balance < wei:
                            st.error("❌ Insufficient balance!")
                        else:
                            with st.spinner("Posting job..."):
                                tx = contract.functions.postJob(desc).build_transaction({
                                    'from': account.address,
                                    'value': wei,
                                    'gas': 300000,
                                    'gasPrice': w3.eth.gas_price,
                                    'nonce': w3.eth.get_transaction_count(account.address)
                                })
                                signed_tx = w3.eth.account.sign_transaction(tx, account.key)
                                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                                st.success(f"✅ Job posted! TX: {tx_hash.hex()}")
                                st.rerun()
                    else:
                        # Brownie transaction
                        if account.balance() < wei:
                            st.error("❌ Insufficient balance!")
                        else:
                            with st.spinner("Posting job..."):
                                tx = contract.postJob(desc, {'from': account, 'value': wei})
                                tx.wait(1)
                                st.success(f"✅ Job posted! TX: {tx.txid}")
                                st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.header("📋 All Jobs")

    try:
        if is_hosted:
            job_count = contract.functions.getJobCount().call()
        else:
            job_count = contract.getJobCount()

        if job_count == 0:
            st.info("No jobs yet. Be the first to post!")
        else:
            for i in range(job_count):
                try:
                    if is_hosted:
                        job = contract.functions.getJob(i).call()
                    else:
                        job = contract.getJob(i)

                    with st.expander(f"#{i} - {job[3][:50]}..." if len(job[3]) > 50 else f"#{i} - {job[3]}"):
                        st.write(f"**Description:** {job[3]}")
                        st.write(f"**Client:** {job[1]}")
                        st.write(f"**Budget:** {Web3.from_wei(job[4], 'ether')} ETH")
                        status_map = {0: "🟢 Open", 1: "🟡 In Progress", 2: "✅ Completed"}
                        st.write(f"**Status:** {status_map.get(job[5], 'Unknown')}")
                        if job[2] != "0x0000000000000000000000000000000000000000":
                            st.write(f"**Freelancer:** {job[2]}")

                        # Action buttons
                        if job[5] == 0 and job[1] != account.address:
                            if st.button(f"✅ Take Job #{i}", key=f"take_{i}"):
                                try:
                                    with st.spinner("Taking job..."):
                                        if is_hosted:
                                            tx = contract.functions.takeJob(i).build_transaction({
                                                'from': account.address,
                                                'gas': 300000,
                                                'gasPrice': w3.eth.gas_price,
                                                'nonce': w3.eth.get_transaction_count(account.address)
                                            })
                                            signed_tx = w3.eth.account.sign_transaction(tx, account.key)
                                            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                                        else:
                                            tx = contract.takeJob(i, {'from': account})
                                            tx.wait(1)
                                        st.success("Job taken!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                        elif job[5] == 1 and job[1] == account.address:
                            if st.button(f"🎉 Complete Job #{i}", key=f"complete_{i}"):
                                try:
                                    with st.spinner("Completing job..."):
                                        if is_hosted:
                                            tx = contract.functions.completeJob(i).build_transaction({
                                                'from': account.address,
                                                'gas': 300000,
                                                'gasPrice': w3.eth.gas_price,
                                                'nonce': w3.eth.get_transaction_count(account.address)
                                            })
                                            signed_tx = w3.eth.account.sign_transaction(tx, account.key)
                                            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                                        else:
                                            tx = contract.completeJob(i, {'from': account})
                                            tx.wait(1)
                                        st.success("Job completed!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                except Exception as e:
                    st.warning(f"Could not load job #{i}: {e}")
    except Exception as e:
        st.error(f"Error fetching jobs: {e}")

# RIGHT: Stats + Tools
with col2:
    st.header("📊 Stats")
    try:
        if is_hosted:
            total = contract.functions.getJobCount().call()
        else:
            total = contract.getJobCount()

        open_, inprog, done = 0, 0, 0
        for i in range(total):
            if is_hosted:
                job = contract.functions.getJob(i).call()
            else:
                job = contract.getJob(i)
            if job[5] == 0: open_ += 1
            elif job[5] == 1: inprog += 1
            elif job[5] == 2: done += 1
        st.metric("Total Jobs", total)
        st.metric("🟢 Open", open_)
        st.metric("🟡 In Progress", inprog)
        st.metric("✅ Completed", done)
    except Exception as e:
        st.error(f"Stats error: {e}")

    st.markdown("---")
    st.header("⚙️ Utilities")
    if st.button("🔄 Refresh"):
        st.rerun()
    if st.button("📜 Show Contract"):
        if is_hosted:
            st.code(f"Address: {contract_address}")
            st.code(f"Network: Web3 Mode")
        else:
            st.code(f"Address: {contract.address}")
            st.code(f"Network: {network.show_active()}")

st.markdown("---")
st.markdown("🚀 **FreelanceX** — Connecting clients & freelancers on the blockchain.")
