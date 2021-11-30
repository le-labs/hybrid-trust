import sc_helper as sh
from web3 import Web3


class middleware:
    def __init__(self, VERBOSE):
        self.VERBOSE = VERBOSE
        # compile and deploy the smart contract
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        w3_accounts = self.w3.eth.get_accounts()

        sc_owner = w3_accounts[0]
        self.w3.eth.defaultAccount = sc_owner
        self.contract = sh.compile_and_deploy(self.w3, 'HybridTrustPLPKI.sol', compiler_version='0.7.6')

    def get_w3_accounts(self):
        return self.w3.eth.get_accounts()

    def hash(self, input):
        hash = self.w3.keccak(input)
        return hash

    def ca_trusts_ca(self, ca_origin, ca_destination):
        sh.transact(self.w3, self.contract.functions.addTrustedCA(ca_destination).transact({'from': ca_origin}))

    def ca_revokes_trust_in_ca(self, ca_origin, ca_destination):
        sh.transact(self.w3, self.contract.functions.removeTrustedCA(ca_destination).transact({'from': ca_origin}))

    def get_trusted_cas(self, ca):
        return self.contract.functions.getTrustedCA(ca).call()

    def add_certificate(self, ca_origin, cert_hash: str, validity_not_before: int, validity_not_after: int,
                        self_destroy_hash: bytes):
        sh.transact(self.w3, self.contract.functions.addCertificate(cert_hash, validity_not_before, validity_not_after,
                                                                    self_destroy_hash).transact(
            {'from': ca_origin}), print_info=self.VERBOSE)

    def retrieve_certificate_status(self, cert_hash, ca):
        print(f"status of certificate {cert_hash}:")
        certificate_status = self.contract.functions.retrieveCertificateStatus(cert_hash, ca).call()
        print(certificate_status)
        return certificate_status

    def revoke_certificate_as_ca(self, ca_origin, cert_hash: str):
        sh.transact(self.w3, self.contract.functions.revokeCertificateAsCA(cert_hash).transact(
            {'from': ca_origin}), print_info=self.VERBOSE)

    def revoke_certificate_as_owner(self, ca_origin, cert_hash: str, ca: str, self_destroy_secret: bytes):
        sh.transact(self.w3,
                    self.contract.functions.revokeCertificateAsHolder(cert_hash, ca, self_destroy_secret).transact(
                        {'from': ca_origin}), print_info=self.VERBOSE)
