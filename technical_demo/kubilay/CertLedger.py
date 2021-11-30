from web3 import Web3
import sc_helper as sh

VERBOSE = False


def get_certificate_count():
    print("number of certificates stored in the smart contract:")
    tls_certificate_count = cert_ledger_contract.functions.retrieveTlsCertificateCount().call()
    print(tls_certificate_count)
    return tls_certificate_count


def get_ca_count():
    print("number of CAs stored in the smart contract:")
    ca_certificate_count = cert_ledger_contract.functions.retrieveCaCertificateCount().call()
    print(ca_certificate_count)
    return ca_certificate_count


def retrieve_certificate_status(cert_hash):
    print(f"status of certificate {cert_hash}:")
    certificate_status = cert_ledger_contract.functions.retrieveCertificateStatus(cert_hash).call()
    print(certificate_status)
    return certificate_status


def retrieve_certificate_value(cert_hash):
    print(f"value of certificate {cert_hash}:")
    certificate_value = cert_ledger_contract.functions.retrieveCertificateValue(cert_hash).call()
    print(certificate_value)
    return certificate_value


def retrieve_ca_status(ca_cert_hash):
    print(f"status of ca {ca_cert_hash}:")
    certificate_status = cert_ledger_contract.functions.retrieveCaCertificateStatus(ca_cert_hash).call()
    print(certificate_status)
    return certificate_status


def retrieve_ca_value(ca_cert_hash):
    print(f"value of ca {ca_cert_hash}:")
    certificate_value = cert_ledger_contract.functions.retrieveCaCertificateValue(ca_cert_hash).call()
    print(certificate_value)
    return certificate_value


# compile and deploy the smart contract
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.defaultAccount = w3.eth.accounts[0]

cert_ledger_contract = sh.compile_and_deploy(w3, 'CertLedgerSmartContract.sol', compiler_version='0.4.25')

# TLS mock hash
cert_hash = Web3.toChecksumAddress('8a64f084f09e82fef5af489d809e47ff91b4f8a4')
# CA hash
ca_cert_hash = Web3.toChecksumAddress('2bc24a613240b15be1df74e018c1cfecc1ef3a2e')

# add a CA
assert get_ca_count() == 0
print("add a CA")
sh.transact(w3, cert_ledger_contract.functions.addCACertificate(ca_cert_hash,
                                                                b'placeholder_certificate_in_X.509_form',
                                                                b'mockup_signatures_of_CertLedger_board').transact(),
            print_info=VERBOSE)
assert get_ca_count() == 1

# add a Certificate
assert get_certificate_count() == 0
print("add a certificate")
sh.transact(w3, cert_ledger_contract.functions.addCertificate(cert_hash,
                                                              b'placeholder_certificate_in_X.509_form').transact(),
            print_info=VERBOSE)

assert get_certificate_count() == 1

print("retrievable information from chain:")
assert retrieve_certificate_status(cert_hash) == 1  # certificate is valid
retrieve_certificate_value(cert_hash)
assert retrieve_ca_status(ca_cert_hash) == 1  # ca is trusted
retrieve_ca_value(ca_cert_hash)

# revoke a certificate
print("revoke a certificate")
sh.transact(w3, cert_ledger_contract.functions.revokeCertificate(cert_hash,
                                                                 b'signed by the private key of the TLS certificate or by the private key of the issuer of the TLS certificate').transact(),
            print_info=VERBOSE)
assert retrieve_certificate_status(cert_hash) == 0  # certificate is invalid

# untrust CA
print("untrust CA")
sh.transact(w3, cert_ledger_contract.functions.untrustCaCertificate(ca_cert_hash,
                                                                    b'signed by the private keys of the CertLedger board').transact(),
            print_info=VERBOSE)
assert retrieve_ca_status(ca_cert_hash) == 0 # ca is untrusted

