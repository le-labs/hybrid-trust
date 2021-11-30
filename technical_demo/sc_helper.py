import solcx
import pprint


def compile_and_deploy(w3, contract_source_path, compiler_version):
    try:
        solcx.set_solc_version(compiler_version)
    except:
        solcx.install_solc(compiler_version)
        solcx.set_solc_version(compiler_version)

    # Compile contract
    with open(contract_source_path, 'r') as f:
        source = f.read()
    compiled_sol = solcx.compile_source(source)

    contract_id, contract_interface = compiled_sol.popitem()

    # Deploy contract
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor().transact()

    # Wait until the contract is included in a block on chain
    w3.eth.waitForTransactionReceipt(tx_hash, timeout=120, poll_latency=0.1)

    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']

    print(f'Deployed {contract_id} to: {address}\n')

    contract = w3.eth.contract(address=address, abi=contract_interface["abi"])

    return contract


def transact(w3, tx_hash, print_info=False):
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    if print_info:
        print("Transaction receipt mined:")
        pprint.pprint(dict(receipt))
        print("Was transaction successful?")
        pprint.pprint(receipt["status"])
        print("")

