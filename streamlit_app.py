import streamlit as st
import os
import sys
from pathlib import Path
from web3 import Web3

# Set working directory to script directory (safe for both CLI and Streamlit)
if "__file__" in globals():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Debug Info
st.sidebar.header("🔧 Debug Info")
st.sidebar.write(f"**Current Directory:** {os.getcwd()}")
st.sidebar.write(f"**Python Path:** {sys.executable}")

# Check Brownie structure
if not os.path.exists("contracts") or not os.path.exists("build"):
    st.error("❌ Not in a valid Brownie project directory.")
    st.stop()

contract_file = Path("build/contracts/FreelanceX.json")
if not contract_file.exists():
    st.error("❌ FreelanceX contract not compiled!")
    st.error("Run: `brownie compile`")
    st.stop()

# Import contract
FreelanceX = None
try:
    from brownie import FreelanceX, accounts, network
    st.sidebar.success("✅ Brownie import successful!")
except ImportError:
    try:
        from brownie.project import load
        from brownie import accounts, network
        proj = load(".", name="FreelanceX", raise_if_loaded=False)
        FreelanceX = getattr(proj, "FreelanceX", None)
        if FreelanceX is None:
            st.error("❌ Contract 'FreelanceX' not found in loaded project.")
            st.stop()
        st.sidebar.success("✅ Fallback project load successful!")
    except Exception as e:
        st.error(f"❌ Failed to load contract: {e}")
        st.stop()

# Connect to local development network
def connect():
    try:
        if network.show_active() != "development":
            network.connect("development")
        return accounts
    except Exception as e:
        st.error(f"⚠️ Network error: {e}")
        st.stop()

accounts_list = connect()
if not accounts_list:
    st.stop()

st.set_page_config(page_title="FreelanceX", layout="wide")
st.title("🧑‍💻 FreelanceX - Decentralized Freelancing Platform")

# Sidebar account info
with st.sidebar:
    st.header("🔗 Connection Info")
    try:
        st.write(f"**Network:** {network.show_active()}")
        account_addresses = [acct.address for acct in accounts_list]
        selected_address = st.selectbox("👛 Select Wallet", account_addresses)

        # Find the actual account object again using its address
        account = next(acct for acct in accounts_list if acct.address == selected_address)

        st.write(f"**Address:** {selected_address}")
        st.write(f"**Balance:** {account.balance() / 10**18:.4f} ETH")

        st.write(f"**Balance:** {account.balance() / 10**18:.4f} ETH")
    except Exception as e:
        st.error(f"⚠️ Account error: {e}")
        st.stop()

# Load deployed contract or deploy if missing
try:
    if len(FreelanceX) == 0:
        st.warning("⚠️ No deployed FreelanceX contract found.")
        if st.button("🚀 Deploy Contract"):
            with st.spinner("Deploying..."):
                try:
                    contract = FreelanceX.deploy({'from': account})
                    st.success(f"✅ Contract deployed at {contract.address}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Deployment failed: {e}")
        st.stop()
    contract = FreelanceX[-1]
    st.success(f"✅ Connected to contract at {contract.address}")
except Exception as e:
    st.error(f"❌ Error accessing deployed contract: {e}")
    st.stop()

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
                    tx = contract.postJob(desc, {'from': account, 'value': wei})
                    tx.wait(1)
                    st.success(f"✅ Job posted! TX: {tx.txid}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.header("📋 All Jobs")

    try:
        job_count = contract.getJobCount()
        if job_count == 0:
            st.info("No jobs yet. Be the first to post!")
        else:
            for i in range(job_count):
                try:
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
                                    tx = contract.takeJob(i, {'from': account})
                                    tx.wait(1)
                                    st.success("Job taken!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {e}")
                        elif job[5] == 1 and job[1] == account.address:
                            if st.button(f"🎉 Complete Job #{i}", key=f"complete_{i}"):
                                try:
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
        total = contract.getJobCount()
        open_, inprog, done = 0, 0, 0
        for i in range(total):
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
        st.code(f"Address: {contract.address}")
        st.code(f"Network: {network.show_active()}")

st.markdown("---")
st.markdown("🚀 **FreelanceX** — Connecting clients & freelancers on the blockchain.")
