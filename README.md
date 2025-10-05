# FreelanceX - Decentralized Freelancing Platform

A blockchain-based freelancing platform built with Solidity smart contracts and Streamlit frontend, enabling transparent job posting, hiring, and payment processing through smart contracts.

## 🎯 Project Overview

FreelanceX is a decentralized application (dApp) that connects clients and freelancers through blockchain technology, ensuring transparent transactions and eliminating intermediary fees.

### Key Features
- **Smart Contract Jobs**: Post and manage jobs on-chain
- **Escrow System**: Automatic payment holding and release
- **Multi-Account Support**: Switch between different wallet accounts
- **Real-time Stats**: Track job statistics and platform metrics
- **Local Development**: Full Brownie integration for testing

## 🏗️ Architecture

### Tech Stack
- **Smart Contracts**: Solidity (Ethereum/Sepolia)
- **Development Framework**: Brownie
- **Frontend**: Python + Streamlit
- **Blockchain Interaction**: Web3.py
- **Testing**: Brownie testing framework

### Contract Structure
```solidity
contract FreelanceX {
    struct Job {
        uint256 id;
        address payable client;
        address payable freelancer;
        string description;
        uint256 budget;
        Status status;
    }

    enum Status { Open, InProgress, Completed }
}
```

## 📁 Project Structure

```
FreelanceX/
├── contracts/
│   └── FreelanceX.sol          # Main smart contract
├── scripts/
│   └── deploy.py               # Deployment script
├── tests/
│   └── test_freelancex.py      # Contract tests
├── build/
│   └── contracts/              # Compiled contracts (auto-generated)
├── streamlit_app.py            # Main frontend application
├── brownie-config.yaml         # Brownie configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for Brownie)
- Git

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/vedang18200/FreelanceX.git
cd FreelanceX
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Brownie**
```bash
pip install eth-brownie
```

4. **Compile Contracts**
```bash
brownie compile
```

5. **Run Local Blockchain**
```bash
brownie console
# This starts local Ganache instance
```

6. **Deploy Contract**
```bash
brownie run scripts/deploy.py
```

7. **Launch Frontend**
```bash
streamlit run streamlit_app.py
```

## 💼 Usage Workflow

### For Clients
1. **Connect Wallet**: Select account from sidebar
2. **Post Job**: Fill description and set budget in ETH
3. **Wait for Applications**: Freelancers can take your job
4. **Complete Job**: Mark job as complete to release payment

### For Freelancers
1. **Browse Jobs**: View all available jobs
2. **Take Job**: Click "Take Job" on open positions
3. **Work & Deliver**: Complete the work as described
4. **Get Paid**: Client marks complete and payment is released

### Platform Flow
```
Client Posts Job → Freelancer Takes Job → Work Completion → Payment Release
      ↓                    ↓                     ↓              ↓
   [Open]            [In Progress]         [In Progress]   [Completed]
```

## 🔧 Development

### Local Testing
```bash
# Compile contracts
brownie compile

# Run tests
brownie test

# Deploy to local network
brownie run scripts/deploy.py

# Launch Streamlit app
streamlit run streamlit_app.py
```

### Network Configuration
- **Local**: Ganache (automatic with Brownie)
- **Testnet**: Sepolia (configured in brownie-config.yaml)
- **Mainnet**: Ethereum (for production)

## 📊 Smart Contract Functions

### Core Functions
- `postJob(string _description)`: Create new job with ETH budget
- `takeJob(uint256 _jobId)`: Freelancer accepts job
- `completeJob(uint256 _jobId)`: Client marks job complete
- `getJob(uint256 _jobId)`: Retrieve job details
- `getAllJobs()`: Get all jobs array
- `getJobCount()`: Get total number of jobs

### Events
- `JobPosted(uint256 jobId, address client, string description, uint256 budget)`
- `JobTaken(uint256 jobId, address freelancer)`
- `JobCompleted(uint256 jobId)`

## 🧪 Testing

### Contract Tests
```bash
brownie test -v
```

### Frontend Testing
```bash
streamlit run streamlit_app.py
# Navigate to http://localhost:8501
```

## 📈 Current Status

### Implemented Features ✅
- [x] Smart contract development
- [x] Local Brownie integration
- [x] Streamlit frontend
- [x] Job posting/taking/completion
- [x] Multi-account wallet support
- [x] Real-time statistics
- [x] Local development environment

### Future Enhancements 🚧
- [ ] Dispute resolution system
- [ ] Rating and review system
- [ ] Multiple payment tokens
- [ ] Advanced filtering and search
- [ ] Mobile-responsive design
- [ ] IPFS integration for file sharing

## 🔐 Security Considerations

- **Escrow Protection**: Funds locked until job completion
- **Access Control**: Only clients can complete their jobs
- **State Management**: Proper job status transitions
- **Input Validation**: Description and amount checks

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Developer**: Vedang Deshmukh
- **GitHub**: [@vedang18200](https://github.com/vedang18200)

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check documentation in `/docs` folder
- Review test files for usage examples

---

**FreelanceX** - Revolutionizing freelancing through blockchain technology 🚀
