from web3 import Web3
import web3 as web3_h
import pprint
from sc_helper import compile_and_deploy

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.defaultAccount = w3.eth.accounts[0]

scpki_contract = compile_and_deploy(w3, 'trustery.sol', compiler_version='0.4.24')

tx_hash = scpki_contract.functions.addAttribute('DomainCertificate', True, b'0000', 'Content of Certificate', 'hashOfData').transact()

# scpki_contract.getPastEvents()
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Transaction receipt mined:")
pprint.pprint(dict(receipt))
print("\nWas transaction successful?")
pprint.pprint(receipt["status"])

