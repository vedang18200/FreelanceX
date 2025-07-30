import streamlit as st
from web3 import Web3

# Try to import the deployed contract
try:
    from brownie.project import FreelancexProject
    from brownie import accounts, network
    FreelanceX = FreelancexProject.FreelanceX
except ImportError as e:
    st.error("⚠️ Could not import the FreelanceX contract. Make sure you're running this from the Brownie project root.")
    st.stop()

# Connect to Brownie development network
def connect():
    if network.show_active() != "development":
        network.connect("development")
    return accounts

accounts = connect()

st.set_page_config(page_title="FreelanceX", layout="centered")
st.title("🧑‍💻 FreelanceX - Decentralized Freelancing Platform")

account = st.selectbox("👛 Select Your Wallet", accounts)

# Get latest deployed contract
try:
    contract = FreelanceX[-1]
except IndexError:
    st.error("⚠️ No FreelanceX contract deployed. Please run the deployment script first.")
    st.stop()

st.markdown("---")

# 🚀 Post a Job
st.header("📢 Post a Job")
desc = st.text_input("📝 Job Description")
eth = st.text_input("💰 Budget in ETH", value="0.1")

if st.button("📤 Post Job"):
    try:
        budget_wei = Web3.toWei(float(eth), 'ether')
        tx = contract.postJob(desc, {'from': account, 'value': budget_wei})
        tx.wait(1)
        st.success("✅ Job posted successfully!")
    except ValueError:
        st.error("❌ Invalid ETH amount.")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

st.markdown("---")

# 🔍 View a Job
st.header("📃 View Job")
job_id = st.number_input("🔎 Job ID", min_value=0, step=1)

if st.button("🔍 Get Job"):
    try:
        job = contract.getJob(job_id)
        st.json({
            "ID": job[0],
            "Client": job[1],
            "Freelancer": job[2],
            "Description": job[3],
            "Budget (ETH)": Web3.fromWei(job[4], 'ether'),
            "Status": ["Open", "InProgress", "Completed"][job[5]],
        })
    except Exception as e:
        st.error(f"⚠️ Error fetching job: {str(e)}")

st.markdown("---")

# 🛠 Take a Job
st.header("💼 Take Job")
job_id_take = st.number_input("Enter Job ID to Take", min_value=0, step=1, key="take_job")

if st.button("✅ Take Job"):
    try:
        tx = contract.takeJob(job_id_take, {'from': account})
        tx.wait(1)
        st.success("🙌 Job successfully taken!")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# ✅ Complete a Job
st.header("✅ Complete Job")
job_id_complete = st.number_input("Enter Job ID to Complete", min_value=0, step=1, key="complete_job")

if st.button("🎉 Complete Job"):
    try:
        tx = contract.completeJob(job_id_complete, {'from': account})
        tx.wait(1)
        st.success("🎊 Job completed and payment released!")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
