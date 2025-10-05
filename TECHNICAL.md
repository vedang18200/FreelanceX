# FreelanceX Technical Documentation

## Smart Contract Architecture

### Contract: FreelanceX.sol

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FreelanceX {
    struct Job {
        uint256 id;
        address payable client;
        address payable freelancer;
        string description;
        uint256 budget;
        Status status;
    }

    enum Status {
        Open,       // 0 - Job posted, accepting applications
        InProgress, // 1 - Job taken by freelancer
        Completed   // 2 - Job completed, payment released
    }

    mapping(uint256 => Job) public jobs;
    uint256 public nextJobId;

    event JobPosted(uint256 indexed jobId, address indexed client, string description, uint256 budget);
    event JobTaken(uint256 indexed jobId, address indexed freelancer);
    event JobCompleted(uint256 indexed jobId);
}
```

### State Variables
- `jobs`: Mapping of job ID to Job struct
- `nextJobId`: Counter for generating unique job IDs

### Function Analysis

#### `postJob(string memory _description)`
- **Access**: Public, Payable
- **Purpose**: Create new job with ETH budget
- **Requirements**: msg.value > 0, non-empty description
- **State Changes**: Creates new job, increments nextJobId
- **Events**: Emits JobPosted

#### `takeJob(uint256 _jobId)`
- **Access**: Public
- **Purpose**: Freelancer accepts an open job
- **Requirements**: Job exists, status is Open, caller is not client
- **State Changes**: Sets freelancer, changes status to InProgress
- **Events**: Emits JobTaken

#### `completeJob(uint256 _jobId)`
- **Access**: Public
- **Purpose**: Client marks job complete and releases payment
- **Requirements**: Job exists, status is InProgress, caller is client
- **State Changes**: Sets status to Completed, transfers funds to freelancer
- **Events**: Emits JobCompleted

## Frontend Architecture

### Streamlit Application Structure

```python
# Main Components
1. Sidebar - Wallet & Network Info
2. Left Column - Job Management
3. Right Column - Statistics & Utilities
```

### Key Functions

#### `connect()`
- Connects to Brownie development network
- Returns available accounts
- Handles network errors

#### Job Display Logic
```python
for i in range(job_count):
    job = contract.getJob(i)
    # job[0] = id
    # job[1] = client
    # job[2] = freelancer
    # job[3] = description
    # job[4] = budget (wei)
    # job[5] = status (0,1,2)
```

### State Management
- Uses `st.rerun()` for real-time updates
- Form-based input validation
- Error handling with try-catch blocks

## Development Environment

### Brownie Configuration
```yaml
# brownie-config.yaml
dependencies:
  - OpenZeppelin/openzeppelin-contracts@4.8.0

compiler:
  solc:
    version: 0.8.19

networks:
  development:
    host: http://127.0.0.1:8545
  sepolia:
    host: https://sepolia.infura.io/v3/$WEB3_INFURA_PROJECT_ID
```

### Python Dependencies
```txt
streamlit>=1.28.0
eth-brownie>=1.19.0
web3>=6.0.0
pathlib
```

## Testing Framework

### Contract Tests Structure
```python
import pytest
from brownie import FreelanceX, accounts

def test_post_job():
    # Deploy contract
    # Post job with ETH
    # Verify job created

def test_take_job():
    # Post job
    # Take job from different account
    # Verify status change

def test_complete_job():
    # Post and take job
    # Complete job as client
    # Verify payment transfer
```

## Gas Optimization

### Function Gas Estimates
- `postJob()`: ~50,000 gas
- `takeJob()`: ~30,000 gas
- `completeJob()`: ~35,000 gas
- `getJob()`: ~5,000 gas (view)

### Optimization Strategies
- Use `uint256` for IDs (gas efficient)
- Pack struct variables efficiently
- Minimize storage writes
- Use events for off-chain data

## Security Analysis

### Access Control
```solidity
modifier onlyClient(uint256 _jobId) {
    require(jobs[_jobId].client == msg.sender, "Only client can call");
    _;
}
```

### Reentrancy Protection
- State changes before external calls
- Use `.transfer()` instead of `.call()`
- Consider OpenZeppelin's ReentrancyGuard

### Input Validation
- Check job existence
- Validate status transitions
- Ensure non-zero amounts

## Deployment Guide

### Local Deployment
```bash
brownie console
>>> accounts[0]
>>> FreelanceX.deploy({'from': accounts[0]})
```

### Testnet Deployment
```bash
brownie run scripts/deploy.py --network sepolia
```

### Production Considerations
- Multi-signature wallet integration
- Upgrade proxy patterns
- Emergency pause mechanisms
- Formal verification

## Performance Metrics

### Current Limitations
- Single contract instance
- No pagination for jobs
- Basic search functionality
- Limited error handling

### Scalability Solutions
- Job factory pattern
- Off-chain indexing
- Layer 2 integration
- IPFS for metadata

## API Reference

### Contract Methods
```javascript
// Read Methods
getJob(uint256 _jobId) → (id, client, freelancer, description, budget, status)
getJobCount() → uint256
getAllJobs() → Job[]

// Write Methods
postJob(string _description) payable
takeJob(uint256 _jobId)
completeJob(uint256 _jobId)
```

### Frontend API
```python
# Streamlit Components
st.form("post_job")
st.selectbox("👛 Select Wallet", account_addresses)
st.expander(f"#{i} - {job[3]}")
st.metric("Total Jobs", total)
```

## Troubleshooting

### Common Issues
1. **Contract not compiled**: Run `brownie compile`
2. **Network connection**: Check Ganache is running
3. **Account balance**: Ensure sufficient ETH for gas
4. **Transaction fails**: Check function requirements

### Debug Commands
```bash
brownie console --network development
>>> network.show_active()
>>> accounts[0].balance()
>>> FreelanceX.at("0x...")
```
