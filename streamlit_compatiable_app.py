import streamlit as st
import json
import os
from web3 import Web3
from eth_account import Account

# Streamlit Cloud Configuration
st.set_page_config(page_title="FreelanceX", layout="wide")

def get_web3_connection():
    """Connect to Ethereum network"""
    # Use public RPC endpoints for different networks
    networks = {
        "Sepolia Testnet": "https://sepolia.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
        "Polygon Mumbai": "https://rpc-mumbai.maticvigil.com/",
        "Ethereum Mainnet": "https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"
    }

    selected_network = st.sidebar.selectbox("🌐 Select Network", list(networks.keys()))
    rpc_url = networks[selected_network]

    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if w3.is_connected():
            st.sidebar.success(f"✅ Connected to {selected_network}")
            return w3, selected_network
        else:
            st.sidebar.error("❌ Failed to connect to network")
            return None, None
    except Exception as e:
        st.sidebar.error(f"Connection error: {e}")
        return None, None

def load_contract_abi():
    """Load the actual FreelanceX contract ABI"""
    return [
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "jobId",
                    "type": "uint256"
                }
            ],
            "name": "JobCompleted",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "jobId",
                    "type": "uint256"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "client",
                    "type": "address"
                },
                {
                    "indexed": False,
                    "internalType": "string",
                    "name": "description",
                    "type": "string"
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "budget",
                    "type": "uint256"
                }
            ],
            "name": "JobPosted",
            "type": "event"
        },
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "uint256",
                    "name": "jobId",
                    "type": "uint256"
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "freelancer",
                    "type": "address"
                }
            ],
            "name": "JobTaken",
            "type": "event"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_jobId",
                    "type": "uint256"
                }
            ],
            "name": "completeJob",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getAllJobs",
            "outputs": [
                {
                    "components": [
                        {
                            "internalType": "uint256",
                            "name": "id",
                            "type": "uint256"
                        },
                        {
                            "internalType": "address payable",
                            "name": "client",
                            "type": "address"
                        },
                        {
                            "internalType": "address payable",
                            "name": "freelancer",
                            "type": "address"
                        },
                        {
                            "internalType": "string",
                            "name": "description",
                            "type": "string"
                        },
                        {
                            "internalType": "uint256",
                            "name": "budget",
                            "type": "uint256"
                        },
                        {
                            "internalType": "enum FreelanceX.Status",
                            "name": "status",
                            "type": "uint8"
                        }
                    ],
                    "internalType": "struct FreelanceX.Job[]",
                    "name": "",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_jobId",
                    "type": "uint256"
                }
            ],
            "name": "getJob",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "id",
                    "type": "uint256"
                },
                {
                    "internalType": "address",
                    "name": "client",
                    "type": "address"
                },
                {
                    "internalType": "address",
                    "name": "freelancer",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "description",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "budget",
                    "type": "uint256"
                },
                {
                    "internalType": "enum FreelanceX.Status",
                    "name": "status",
                    "type": "uint8"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getJobCount",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "name": "jobs",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "id",
                    "type": "uint256"
                },
                {
                    "internalType": "address payable",
                    "name": "client",
                    "type": "address"
                },
                {
                    "internalType": "address payable",
                    "name": "freelancer",
                    "type": "address"
                },
                {
                    "internalType": "string",
                    "name": "description",
                    "type": "string"
                },
                {
                    "internalType": "uint256",
                    "name": "budget",
                    "type": "uint256"
                },
                {
                    "internalType": "enum FreelanceX.Status",
                    "name": "status",
                    "type": "uint8"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "nextJobId",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "string",
                    "name": "_description",
                    "type": "string"
                }
            ],
            "name": "postJob",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "_jobId",
                    "type": "uint256"
                }
            ],
            "name": "takeJob",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]

def get_contract_address():
    """Get contract address from Streamlit secrets"""
    try:
        # Try to get from Streamlit secrets first
        return st.secrets["FREELANCEX_CONTRACT_ADDRESS"]
    except:
        # Fallback to environment variable
        address = os.getenv("FREELANCEX_CONTRACT_ADDRESS")
        if not address:
            st.error("❌ Contract address not found!")
            st.error("Add FREELANCEX_CONTRACT_ADDRESS to your Streamlit secrets")
            st.stop()
        return address

def get_account_from_private_key():
    """Get account from private key (optional for read-only mode)"""
    try:
        # Try to get from Streamlit secrets
        private_key = st.secrets.get("PRIVATE_KEY", "")
        if private_key:
            account = Account.from_key(private_key)
            return account
        return None
    except:
        return None

# Main App
st.title("🧑‍💻 FreelanceX - Decentralized Freelancing Platform")

# Sidebar
with st.sidebar:
    st.header("🔗 Connection Info")

    # Network connection
    w3, network_name = get_web3_connection()
    if not w3:
        st.stop()

    # Contract setup
    contract_address = get_contract_address()
    contract_abi = load_contract_abi()

    try:
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        st.success(f"✅ Contract loaded")
        st.write(f"**Address:** {contract_address}")
    except Exception as e:
        st.error(f"❌ Contract error: {e}")
        st.stop()

    # Account info
    account = get_account_from_private_key()
    if account:
        st.write(f"**Wallet:** {account.address}")
        try:
            balance = w3.eth.get_balance(account.address)
            st.write(f"**Balance:** {w3.from_wei(balance, 'ether'):.4f} ETH")
        except:
            st.write("**Balance:** Unable to fetch")
    else:
        st.warning("⚠️ No private key - Read-only mode")

# Main layout
col1, col2 = st.columns([2, 1])

# LEFT: Jobs
with col1:
    # Post Job (only if account available)
    if account:
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
                        # Build transaction
                        nonce = w3.eth.get_transaction_count(account.address)
                        gas_price = w3.eth.gas_price
                        value = w3.to_wei(eth, 'ether')

                        # Estimate gas
                        gas_estimate = contract.functions.postJob(desc).estimate_gas({
                            'from': account.address,
                            'value': value
                        })

                        # Build transaction
                        transaction = contract.functions.postJob(desc).build_transaction({
                            'from': account.address,
                            'value': value,
                            'gas': gas_estimate,
                            'gasPrice': gas_price,
                            'nonce': nonce,
                        })

                        # Sign and send
                        signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
                        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

                        st.success(f"✅ Job posted! TX: {tx_hash.hex()}")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Error: {e}")

    st.markdown("---")
    st.header("📋 All Jobs")

    try:
        # Use the getAllJobs function for better performance
        all_jobs = contract.functions.getAllJobs().call()

        if len(all_jobs) == 0:
            st.info("No jobs yet. Be the first to post!")
        else:
            for job in all_jobs:
                job_id, client, freelancer, description, budget, status = job

                with st.expander(f"#{job_id} - {description[:50]}..." if len(description) > 50 else f"#{job_id} - {description}"):
                    st.write(f"**Description:** {description}")
                    st.write(f"**Client:** {client}")
                    st.write(f"**Budget:** {w3.from_wei(budget, 'ether')} ETH")

                    status_map = {0: "🟢 Open", 1: "🟡 In Progress", 2: "✅ Completed"}
                    st.write(f"**Status:** {status_map.get(status, 'Unknown')}")

                    if freelancer != "0x0000000000000000000000000000000000000000":
                        st.write(f"**Freelancer:** {freelancer}")

                    # Action buttons (only if account available)
                    if account:
                        if status == 0 and client.lower() != account.address.lower():
                            if st.button(f"✅ Take Job #{job_id}", key=f"take_{job_id}"):
                                try:
                                    # Build takeJob transaction
                                    nonce = w3.eth.get_transaction_count(account.address)
                                    gas_estimate = contract.functions.takeJob(job_id).estimate_gas({'from': account.address})

                                    transaction = contract.functions.takeJob(job_id).build_transaction({
                                        'from': account.address,
                                        'gas': gas_estimate,
                                        'gasPrice': w3.eth.gas_price,
                                        'nonce': nonce,
                                    })

                                    signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
                                    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

                                    st.success(f"✅ Job taken! TX: {tx_hash.hex()}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")

                        elif status == 1 and client.lower() == account.address.lower():
                            if st.button(f"🎉 Complete Job #{job_id}", key=f"complete_{job_id}"):
                                try:
                                    # Build completeJob transaction
                                    nonce = w3.eth.get_transaction_count(account.address)
                                    gas_estimate = contract.functions.completeJob(job_id).estimate_gas({'from': account.address})

                                    transaction = contract.functions.completeJob(job_id).build_transaction({
                                        'from': account.address,
                                        'gas': gas_estimate,
                                        'gasPrice': w3.eth.gas_price,
                                        'nonce': nonce,
                                    })

                                    signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
                                    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

                                    st.success(f"✅ Job completed! TX: {tx_hash.hex()}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")

    except Exception as e:
        st.error(f"Error fetching jobs: {e}")

# RIGHT: Stats
with col2:
    st.header("📊 Stats")
    try:
        all_jobs = contract.functions.getAllJobs().call()
        total = len(all_jobs)
        open_, inprog, done = 0, 0, 0

        for job in all_jobs:
            status = job[5]  # status is the 6th element
            if status == 0: open_ += 1
            elif status == 1: inprog += 1
            elif status == 2: done += 1

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

st.markdown("---")
st.markdown("🚀 **FreelanceX** — Connecting clients & freelancers on the blockchain.")
