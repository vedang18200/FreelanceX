# FreelanceX API Documentation

## Smart Contract Interface

### Contract Address
- **Local**: Deployed via Brownie (varies)
- **Testnet**: To be deployed
- **Mainnet**: Not deployed

### ABI Functions

#### Read Functions

##### `getJob(uint256 _jobId)`
**Description**: Retrieve complete job information by ID
**Parameters**:
- `_jobId` (uint256): Unique job identifier
**Returns**:
```solidity
(
    uint256 id,
    address client,
    address freelancer,
    string description,
    uint256 budget,
    uint8 status
)
```
**Example**:
```python
job = contract.getJob(0)
print(f"Job ID: {job[0]}")
print(f"Client: {job[1]}")
print(f"Budget: {job[4]} wei")
```

##### `getJobCount()`
**Description**: Get total number of jobs posted
**Parameters**: None
**Returns**: `uint256` - Total job count
**Example**:
```python
total_jobs = contract.getJobCount()
```

##### `getAllJobs()`
**Description**: Retrieve all jobs in a single call
**Parameters**: None
**Returns**: `Job[]` - Array of all job structs
**Example**:
```python
all_jobs = contract.getAllJobs()
for job in all_jobs:
    print(f"Job {job[0]}: {job[3]}")
```

#### Write Functions

##### `postJob(string _description)`
**Description**: Create new job posting with ETH escrow
**Parameters**:
- `_description` (string): Job description and requirements
**Payable**: Yes - ETH amount becomes job budget
**Requirements**:
- `msg.value > 0`
- `_description` not empty
**Events**: `JobPosted(jobId, client, description, budget)`
**Example**:
```python
tx = contract.postJob("Build a website", {
    'from': account,
    'value': Web3.to_wei(0.1, 'ether')
})
```

##### `takeJob(uint256 _jobId)`
**Description**: Freelancer accepts an open job
**Parameters**:
- `_jobId` (uint256): Job to accept
**Requirements**:
- Job must exist
- Job status must be Open (0)
- Caller cannot be the client
**Events**: `JobTaken(jobId, freelancer)`
**Example**:
```python
tx = contract.takeJob(0, {'from': freelancer_account})
```

##### `completeJob(uint256 _jobId)`
**Description**: Client marks job complete and releases payment
**Parameters**:
- `_jobId` (uint256): Job to complete
**Requirements**:
- Job must exist
- Job status must be InProgress (1)
- Caller must be the client
**Events**: `JobCompleted(jobId)`
**Example**:
```python
tx = contract.completeJob(0, {'from': client_account})
```

### Events

#### `JobPosted`
```solidity
event JobPosted(
    uint256 indexed jobId,
    address indexed client,
    string description,
    uint256 budget
);
```

#### `JobTaken`
```solidity
event JobTaken(
    uint256 indexed jobId,
    address indexed freelancer
);
```

#### `JobCompleted`
```solidity
event JobCompleted(
    uint256 indexed jobId
);
```

## Frontend API

### Streamlit Components

#### Job Posting Form
```python
with st.form("post_job"):
    desc = st.text_area("📝 Job Description")
    eth = st.number_input("💰 Budget (ETH)", min_value=0.001)
    submit = st.form_submit_button("📤 Post Job")
```

#### Wallet Selection
```python
selected_address = st.selectbox("👛 Select Wallet", account_addresses)
account = next(acct for acct in accounts_list if acct.address == selected_address)
```

#### Job Actions
```python
# Take Job Button
if st.button(f"✅ Take Job #{i}", key=f"take_{i}"):
    tx = contract.takeJob(i, {'from': account})

# Complete Job Button
if st.button(f"🎉 Complete Job #{i}", key=f"complete_{i}"):
    tx = contract.completeJob(i, {'from': account})
```

## Error Handling

### Smart Contract Errors
```solidity
require(msg.value > 0, "Budget must be greater than 0");
require(bytes(_description).length > 0, "Description cannot be empty");
require(_jobId < nextJobId, "Job does not exist");
require(jobs[_jobId].status == Status.Open, "Job is not open");
```

### Frontend Error Handling
```python
try:
    tx = contract.postJob(desc, {'from': account, 'value': wei})
    tx.wait(1)
    st.success(f"✅ Job posted! TX: {tx.txid}")
except Exception as e:
    st.error(f"Error: {e}")
```

## Usage Examples

### Complete Job Flow
```python
# 1. Client posts job
tx1 = contract.postJob("Build mobile app", {
    'from': client,
    'value': Web3.to_wei(1, 'ether')
})

# 2. Freelancer takes job
tx2 = contract.takeJob(0, {'from': freelancer})

# 3. Client completes job (releases payment)
tx3 = contract.completeJob(0, {'from': client})
```

### Query Job Information
```python
# Get specific job
job = contract.getJob(0)
print(f"Status: {['Open', 'InProgress', 'Completed'][job[5]]}")

# Get all jobs
jobs = contract.getAllJobs()
open_jobs = [job for job in jobs if job[5] == 0]
```

## Integration Guide

### Web3.py Integration
```python
from web3 import Web3
from brownie import FreelanceX

# Connect to network
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load contract
contract = FreelanceX[-1]  # Latest deployment

# Call functions
result = contract.getJobCount()
```

### Frontend Integration
```python
import streamlit as st
from brownie import FreelanceX, accounts, network

# Setup
if not network.is_connected():
    network.connect("development")

# Use contract
contract = FreelanceX[-1]
job_count = contract.getJobCount()
```

## Rate Limits & Performance

### Transaction Limits
- **Block Gas Limit**: ~30M gas (Ethereum)
- **Function Gas Costs**:
  - `postJob()`: ~50,000 gas
  - `takeJob()`: ~30,000 gas
  - `completeJob()`: ~35,000 gas

### Query Performance
- **Local Node**: ~50ms per call
- **Remote Node**: ~200-500ms per call
- **Batch Queries**: Use `getAllJobs()` for multiple jobs

## Security Considerations

### Access Control
- Only clients can complete their jobs
- Only non-clients can take jobs
- Job status prevents invalid transitions

### Input Validation
- Non-empty descriptions required
- Positive budget amounts only
- Valid job IDs only

### Best Practices
- Always check transaction success
- Handle network failures gracefully
- Validate user inputs client-side
- Use appropriate gas limits

---

*This API documentation covers all public interfaces of the FreelanceX platform.*
