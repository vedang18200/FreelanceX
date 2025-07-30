import streamlit as st
import os
import sys
from pathlib import Path
from web3 import Web3

# Debug information
st.sidebar.header("🔧 Debug Info")
st.sidebar.write(f"**Current Directory:** {os.getcwd()}")
st.sidebar.write(f"**Python Path:** {sys.executable}")

# Check if we're in a Brownie project
if not os.path.exists("contracts"):
    st.error("❌ Not in a Brownie project directory!")
    st.error("Please navigate to your FreelanceX project root directory.")
    st.stop()

if not os.path.exists("build"):
    st.error("❌ Contracts not compiled!")
    st.error("Please run: `brownie compile` first.")
    st.stop()

# Check for compiled FreelanceX contract
freelancex_build = Path("build/contracts/FreelanceX.json")
if not freelancex_build.exists():
    st.error("❌ FreelanceX contract not found in build directory!")
    st.error("Make sure your contract is named 'FreelanceX' and run: `brownie compile`")
    st.stop()

st.sidebar.write("✅ Project structure looks good!")

# Try to import the deployed contract
try:
    from brownie import FreelanceX, accounts, network
    st.sidebar.write("✅ Brownie import successful!")
except ImportError as e:
    st.error("⚠️ Could not import FreelanceX from Brownie.")
    st.error(f"Error details: {str(e)}")
    st.error("**Troubleshooting:**")
    st.error("1. Make sure you're in the Brownie project root directory")
    st.error("2. Run: `brownie compile`")
    st.error("3. Run: `brownie run scripts/deploy.py`")
    st.error("4. Ensure your contract is named 'FreelanceX' in FreelanceX.sol")
    st.stop()

# Connect to Brownie development network
def connect():
    try:
        current_network = network.show_active()
        if current_network != "development":
            st.info(f"Current network: {current_network}")
            st.info("Connecting to development network...")
            network.connect("development")
        return accounts
    except Exception as e:
        st.error(f"⚠️ Network connection error: {str(e)}")
        st.error("Make sure Ganache is running or use: `brownie console`")
        return None

accounts_list = connect()
if accounts_list is None:
    st.stop()

st.set_page_config(page_title="FreelanceX", layout="wide")
st.title("🧑‍💻 FreelanceX - Decentralized Freelancing Platform")

# Sidebar for account selection and info
with st.sidebar:
    st.header("🔗 Connection Info")
    try:
        st.write(f"**Network:** {network.show_active()}")
        account = st.selectbox("👛 Select Your Wallet", accounts_list)
        st.write(f"**Address:** {account}")
        st.write(f"**Balance:** {account.balance() / 10**18:.4f} ETH")
    except Exception as e:
        st.error(f"Connection error: {e}")
        st.stop()

# Get latest deployed contract
try:
    if len(FreelanceX) == 0:
        st.error("⚠️ No FreelanceX contracts deployed!")
        st.error("Please run: `brownie run scripts/deploy.py`")
        
        # Option to deploy from the app
        if st.button("🚀 Deploy Contract Now"):
            with st.spinner("Deploying contract..."):
                try:
                    contract = FreelanceX.deploy({'from': account})
                    st.success(f"✅ Contract deployed at: {contract.address}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Deployment failed: {e}")
        st.stop()
    
    contract = FreelanceX[-1]  # Get the latest deployed contract
    st.success(f"✅ Connected to FreelanceX contract at: {contract.address}")
    
except Exception as e:
    st.error(f"⚠️ Error getting contract: {str(e)}")
    st.stop()

# Main app layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("---")
    
    # 🚀 Post a Job
    st.header("📢 Post a Job")
    with st.form("post_job_form"):
        desc = st.text_area("📝 Job Description", placeholder="Describe the job you need done...")
        eth = st.number_input("💰 Budget in ETH", min_value=0.001, value=0.1, step=0.001, format="%.3f")
        
        submitted = st.form_submit_button("📤 Post Job")
        if submitted:
            if not desc.strip():
                st.error("❌ Please enter a job description")
            else:
                try:
                    with st.spinner("Posting job..."):
                        budget_wei = Web3.toWei(eth, 'ether')
                        tx = contract.postJob(desc, {'from': account, 'value': budget_wei})
                        tx.wait(1)
                    
                    st.success("✅ Job posted successfully!")
                    st.success(f"🧾 Transaction: {tx.txid}")
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")
    
    st.markdown("---")
    
    # 🔍 View Jobs
    st.header("📋 All Jobs")
    
    try:
        job_count = contract.getJobCount()
        if job_count == 0:
            st.info("No jobs posted yet. Be the first to post a job!")
        else:
            for job_id in range(job_count):
                try:
                    job = contract.getJob(job_id)
                    
                    # Create expandable job card
                    with st.expander(f"Job #{job_id}: {job[3][:50]}..." if len(job[3]) > 50 else f"Job #{job_id}: {job[3]}"):
                        col_a, col_b = st.columns([2, 1])
                        
                        with col_a:
                            st.write(f"**Description:** {job[3]}")
                            st.write(f"**Client:** {job[1]}")
                            st.write(f"**Budget:** {Web3.fromWei(job[4], 'ether')} ETH")
                            
                            status_colors = {"0": "🟢 Open", "1": "🟡 In Progress", "2": "✅ Completed"}
                            st.write(f"**Status:** {status_colors.get(str(job[5]), f'Unknown ({job[5]})')}")
                            
                            if job[2] != "0x0000000000000000000000000000000000000000":
                                st.write(f"**Freelancer:** {job[2]}")
                        
                        with col_b:
                            # Action buttons based on job status and user
                            if job[5] == 0:  # Open job
                                if job[1] != account.address:  # Not the client
                                    if st.button(f"✅ Take Job #{job_id}", key=f"take_{job_id}"):
                                        try:
                                            with st.spinner("Taking job..."):
                                                tx = contract.takeJob(job_id, {'from': account})
                                                tx.wait(1)
                                            st.success("🙌 Job taken successfully!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Error: {e}")
                            
                            elif job[5] == 1:  # In progress
                                if job[1] == account.address:  # Is the client
                                    if st.button(f"🎉 Complete Job #{job_id}", key=f"complete_{job_id}"):
                                        try:
                                            with st.spinner("Completing job..."):
                                                tx = contract.completeJob(job_id, {'from': account})
                                                tx.wait(1)
                                            st.success("🎊 Job completed and payment released!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Error: {e}")
                
                except Exception as e:
                    st.error(f"Error loading job {job_id}: {e}")
    
    except Exception as e:
        st.error(f"Error fetching jobs: {e}")

with col2:
    st.header("📊 Stats")
    
    try:
        total_jobs = contract.getJobCount()
        st.metric("Total Jobs", total_jobs)
        
        # Count jobs by status
        open_jobs = 0
        in_progress_jobs = 0
        completed_jobs = 0
        
        for job_id in range(total_jobs):
            try:
                job = contract.getJob(job_id)
                if job[5] == 0:
                    open_jobs += 1
                elif job[5] == 1:
                    in_progress_jobs += 1
                elif job[5] == 2:
                    completed_jobs += 1
            except:
                continue
        
        st.metric("🟢 Open Jobs", open_jobs)
        st.metric("🟡 In Progress", in_progress_jobs)
        st.metric("✅ Completed", completed_jobs)
        
    except Exception as e:
        st.error(f"Error loading stats: {e}")
    
    st.markdown("---")
    st.header("⚙️ Actions")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.button("📜 View Contract"):
        st.code(f"Contract Address: {contract.address}")
        st.code(f"Network: {network.show_active()}")

# Footer
st.markdown("---")
st.markdown("**FreelanceX** - Connecting freelancers and clients on the blockchain 🚀")