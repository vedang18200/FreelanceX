# FreelanceX Development Setup

## Prerequisites

### Required Software
- **Python 3.8+**: Core development language
- **Node.js 14+**: Required for Brownie framework
- **Git**: Version control
- **VS Code**: Recommended IDE (optional)

### Development Tools
```bash
# Install Python packages
pip install eth-brownie streamlit web3

# Verify installations
python --version
node --version
brownie --version
streamlit --version
```

## Quick Setup Guide

### 1. Clone Repository
```bash
git clone https://github.com/vedang18200/FreelanceX.git
cd FreelanceX
```

### 2. Install Dependencies
```bash
# Install Python requirements
pip install -r requirements.txt

# Install Brownie (if not already installed)
pip install eth-brownie
```

### 3. Initialize Brownie
```bash
# Compile contracts
brownie compile

# Verify compilation
ls build/contracts/
# Should see FreelanceX.json
```

### 4. Start Local Blockchain
```bash
# Start Brownie console (auto-starts Ganache)
brownie console

# Or manually start Ganache
ganache-cli --deterministic --accounts 10 --host 0.0.0.0
```

### 5. Deploy Contract
```bash
# In Brownie console
>>> accounts[0]
<Account '0x66aB6D9362d4F35596279692F0251Db635165871'>

>>> FreelanceX.deploy({'from': accounts[0]})
Transaction sent: 0x...
FreelanceX.constructor confirmed - Block: 1   Gas used: 500000 (100.0%)
FreelanceX deployed at: 0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87
```

### 6. Launch Frontend
```bash
# In new terminal (keep Brownie console running)
streamlit run streamlit_app.py

# App will open at http://localhost:8501
```

## Detailed Configuration

### Brownie Configuration
**File**: `brownie-config.yaml`
```yaml
dependencies:
  - OpenZeppelin/openzeppelin-contracts@4.8.0

compiler:
  solc:
    version: 0.8.19
    settings:
      optimizer:
        enabled: true
        runs: 200

networks:
  development:
    host: http://127.0.0.1:8545
    gas_limit: 12000000
    gas_price: 20000000000
```

### Environment Variables
Create `.env` file (optional):
```bash
WEB3_INFURA_PROJECT_ID=your_infura_key_here
ETHERSCAN_TOKEN=your_etherscan_api_key
```

### VS Code Configuration
**File**: `.vscode/settings.json`
```json
{
    "python.defaultInterpreter": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "solidity.compileUsingRemoteVersion": "v0.8.19"
}
```

## Development Workflow

### Daily Development
```bash
# 1. Start development environment
brownie console

# 2. Deploy fresh contract (in console)
>>> FreelanceX.deploy({'from': accounts[0]})

# 3. Launch frontend (new terminal)
streamlit run streamlit_app.py

# 4. Develop with hot reload
# Edit files, Streamlit auto-reloads
```

### Testing Workflow
```bash
# Run contract tests
brownie test

# Run specific test
brownie test tests/test_freelancex.py::test_post_job

# Run with verbose output
brownie test -v -s
```

### Code Changes Workflow
```bash
# 1. Make contract changes
vim contracts/FreelanceX.sol

# 2. Recompile
brownie compile

# 3. Redeploy in console
>>> FreelanceX.deploy({'from': accounts[0]})

# 4. Frontend automatically picks up new deployment
```

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'brownie'"
```bash
pip install eth-brownie
# Or in virtual environment:
source venv/bin/activate
pip install eth-brownie
```

#### "Network 'development' is not defined"
```bash
# Reset Brownie networks
brownie networks delete development
brownie networks add development host=http://127.0.0.1:8545 chainid=1337
```

#### "Contract not compiled"
```bash
# Clean and recompile
brownie compile --all
# Or force recompile
rm -rf build/
brownie compile
```

#### "No deployed contract found"
```bash
# In Brownie console
>>> FreelanceX.deploy({'from': accounts[0]})
# Then refresh Streamlit app
```

#### Streamlit "Connection refused"
```bash
# Check if Ganache is running
brownie console
# Should start local blockchain automatically
```

### Debug Commands
```bash
# Check network status
brownie console
>>> network.show_active()
>>> len(accounts)
>>> accounts[0].balance()

# Check deployments
>>> len(FreelanceX)
>>> FreelanceX[-1].address if len(FreelanceX) > 0 else "None"

# Test contract interaction
>>> contract = FreelanceX[-1]
>>> contract.getJobCount()
```

## Performance Optimization

### Development Speed
- Keep Brownie console open
- Use `--no-compile` flag when not changing contracts
- Cache compiled contracts in CI/CD

### Frontend Performance
- Use `st.cache` for expensive operations
- Minimize contract calls in loops
- Use `getAllJobs()` instead of individual `getJob()` calls

## Security Setup

### Local Development
- Use test accounts only
- Never commit private keys
- Use environment variables for sensitive data

### Production Preparation
- Use hardware wallets
- Enable multi-signature contracts
- Implement access controls

## IDE Configuration

### VS Code Extensions
- **Solidity**: Juan Blanco
- **Python**: Microsoft
- **Brownie**: Brownie Framework
- **GitLens**: Enhanced Git features

### Sublime Text Configuration
```json
{
    "settings": {
        "translate_tabs_to_spaces": true,
        "tab_size": 4
    }
}
```

## Advanced Setup

### Custom Networks
```bash
# Add testnet (in brownie-config.yaml)
networks:
  sepolia:
    host: https://sepolia.infura.io/v3/$WEB3_INFURA_PROJECT_ID
    chainid: 11155111
```

### Contract Verification
```bash
# Publish source code (testnet/mainnet)
brownie run scripts/deploy.py --network sepolia
```

### CI/CD Pipeline
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: brownie test
```

---

*Complete development environment setup for FreelanceX project.*
