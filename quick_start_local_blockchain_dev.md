# Getting to know the local Blockchain and Smart Contracts
For developing, deploying, and testing smart contracts two tools are needed: 
- Truffle
- Ganache

The following guide will give you a general explanation of how to get started, by making use of demo files. The procedure remains the same for compiling & migrating any smart contract.

## Truffle
Truffle is a development environment, testing framework, and pipeline for deploying smart contracts on any Ethereum Virtual Machine (EVM).
```bash
brew install node 
npm install -g truffle
```

### Truffle development folder structure
To initialize a truffle folder run:
```bash
truffle init
```
This will set up a folder with the following files and folders:
```
.
├── contracts
│   └── Migrations.sol
├── migrations
│   └── 1_initial_migration.js
├── test
└── truffle-config.js
```
In the folder contracts, all contracts which should get compiled should be placed. The file `Migrations.sol` is a demo contract.

In the folder migrations, the deployment options for each contract can be specified. The file `1_initial_migration.js` is a demo migration for the contract `Migrations.sol`.

Tests can be placed in the folder test.

The file `truffle-config.js` specifies parameters for compiling (e.g. which compiler version), testing (e.g which testing tool), and for migrating (e.g. which network to deploy).

### Compiling smart contracts
To compile contracts run inside the folder which was initialized:
```bash
truffle compile
```
This will create the additional folder build, containing the builds of all contracts specified in the contracts folder.
```
.
├── build
│   └── contracts
│       └── Migrations.json
```

## Ganache
Ganache is a local blockchain. It can simulate all the features the Ethereum Virtual Machine (EVM) is capable of. On macOS it is installed with the following command:
```bash
brew install --cask ganache
```
### Setting up a local blockchain
After launching Ganache, click on Quickstart (good enough for the beginning). In the following overview, six tabs (Accounts, Blocks, Transactions, Contracts, Events, Logs) and a fixed horizontal status bar can be seen.

The status bar shows the information on the state of the local blockchain. It shows the last mined block, the price of gas (the currency used for transactions in Ethereum, covers the cost of computing your transaction), the gas limit (how many units of gas you want to spend for a transaction), the hardfork (release version of the EVM, see [history of hardforks](https://medium.com/mycrypto/the-history-of-ethereum-hard-forks-6a6dae76d56f)), the network ID, the RPC server and how mining is processed. 

### Accounts
This tab lists all available accounts on the chain. To each account, a balance is assigned, which can be configured during the setup of Ganache. Those accounts are all unlocked and can be used for deploying, transacting, and interacting with Smart Contracts. The address is derived with a hash of the public key, the private key can be shown with the key icon.

### Blocks
In the tab "Blocks" all mined blocks are shown. Block 0 is called the Genesis block and doesn't contain transactions. All following transactions are summarized in blocks. The blocks in the Ethereum network are created by miners. In the settings of Ganache, automine can be enabled. This setting can be used for development because transactions are immediately mined. Ganache can as well be set to mine every e.g. 30 seconds. All incoming transactions in this time window will be mined in one block. Transaction receipts can be acquired after a block is mined.

### Transactions
This tab lists all transactions made with the blockchain. A transaction is every interaction in which the blockchain persists. This could be a contract deployment, a call of a function in a contract (persisting information), or a transaction between two entities.

### Contracts
This tab is only useful in the case of using truffle to build and deploy smart contracts. If this is the case one can link truffle projects to Ganache and see the storage, available functions, etc.

### Events
Events can be emitted of smart contracts. In case a truffle project is linked with Ganache, the events are shown in a decoded version in this tab. Events are useful since other participants can subscribe to them.

### Logs
This tab shows the log of the EVM. The log can be extended to verbose in the settings.


## Migrating smart contracts
Ganache must be running.

Change the Network ID and the address of the RPC Server in the file: `truffle-config.js` to the values shown in the status bar of Ganache. 

Specify the compiler version to the one required of the smart contract.

In the end the file `truffle-config.js` should look similar to:
```javascript
module.exports = {
  networks: {
    development: {
     host: "127.0.0.1",
     port: 7545, 
     network_id: "5777",
    }
  }
  compilers: {
    solc: {
      version: "0.5.1", 
    }
  }
};

```

The contract can be deployed on the local blockchain with:

```bash
truffle migrate
```

# Advanced Build and Deployment
Due to the issue that different contracts require different compilers we decided to evaluate another way for building, deploying and interacting with smart contracts. 

Thereby we make use of the [Web3 python package](https://web3py.readthedocs.io/en/stable/).

To get ready interacting with smart contracts, the following steps need to be taken:

1. Create a python virtual environment inside the project root folder `technical_demo`. And set the virtual environment as Python interpreter.
2. Install the requirements in the virtual environment.
3. Start Ganache locally, and make sure the RPC Server is set to 127.0.0.1:7545 (default setting).
4. Each subfolder of the project root contains a specific smart contract and a python script to build, deploy and interact with the specific smart contract. Required compilers are installed during the process. You should be able to run a script now.
