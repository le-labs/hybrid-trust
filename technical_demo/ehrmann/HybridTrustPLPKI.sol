// SPDX-License-Identifier: MIT
// compiler version must be greater than or equal to 0.7.6 and less than 0.8.0
pragma solidity ^0.7.6;

contract HybridTrustPLPKI {

    struct certificate {
        bool isValid;
        address certificateHash;
        uint validityNotBefore;
        uint validityNotAfter;
        bytes32 selfDestroyHash;
    }

    /* can be extended with:
        bool isStructureValid;
        address hashValue;
        bytes subject;
        bytes issuer;
        uint validityNotBefore;
        uint validityNotAfter;
        uint extendedKeyUsage;
        bytes subjectAlternativeName;
        bytes aki;
        bytes ski;
        bytes tbsCertificateValue;
        bytes publicKey;
        bytes signature;
    */
    // CA Address -> certificate
    mapping(address => certificate[]) caAddress_certificates_map;


    mapping(address => address[]) partnerCAs;

    function addTrustedCA(address _partnerCA) public {
        partnerCAs[msg.sender].push(_partnerCA);
    }

    function getTrustedCA(address ca) public view returns (address[] memory){
        return partnerCAs[ca];
    }


    function removeTrustedCA(address _partnerCA) public {
        //TODO: advanced error handling if you're not the sender (not the CA) or if partner hash is not in list
        address[] storage partnerCAsList = partnerCAs[msg.sender];
        //iterate through array
        uint i = 0;
        while (partnerCAsList[i] != _partnerCA) {
            i++;
        }

        delete partnerCAsList[i];
        // sets parnerCAsList[i] = 0x0000000000000000000000000000000000000000;
    }


    function retrieveCertificateStatus(address certHash, address CA) public view returns (bool){
        //TODO: advanced error handling
        //TODO: add checks for validity before / after
        certificate[] memory _certificates = caAddress_certificates_map[CA];
        uint i = 0;
        while (_certificates[i].certificateHash != certHash) {
            i++;
        }
        return _certificates[i].isValid;
    }


    function addCertificate(address certHash, uint validityNotBefore, uint validityNotAfter, bytes32 selfDestroyHash) public {
        //TODO: advanced error handling in case certificate exists
        certificate memory _certificate;
        _certificate.isValid = true;
        _certificate.certificateHash = certHash;
        _certificate.validityNotBefore = validityNotBefore;
        _certificate.validityNotAfter = validityNotAfter;
        _certificate.selfDestroyHash = selfDestroyHash;
        caAddress_certificates_map[msg.sender].push(_certificate);
    }

    function revokeCertificateAsCA(address certHash) public {
        //TODO: advanced error handling
        certificate[] storage _certificates = caAddress_certificates_map[msg.sender];

        uint i = 0;
        while (_certificates[i].certificateHash != certHash) {
            i++;
        }

        _certificates[i].isValid = false;
    }

    function revokeCertificateAsHolder(address certHash, address CA, bytes calldata selfDestroySecret) public {
        //TODO: advanced error handling
        bytes32 _selfDestroyHash = keccak256(selfDestroySecret);
        certificate[] storage _certificates = caAddress_certificates_map[CA];

        uint i = 0;
        while (_certificates[i].certificateHash != certHash) {
            i++;
        }
        if (_selfDestroyHash == _certificates[i].selfDestroyHash) {
            _certificates[i].isValid = false;
            return;
        }
        revert(string(abi.encodePacked("Hashes don't match! Hash 1:", bytes32ToString(_selfDestroyHash), " Hash 2:", bytes32ToString(_certificates[i].selfDestroyHash))));
    }

    function bytes32ToString(bytes32 x) public returns (string memory) {
        bytes memory bytesString = new bytes(32);
        uint charCount = 0;
        for (uint j = 0; j < 32; j++) {
            byte char = byte(bytes32(uint(x) * 2 ** (8 * j)));
            if (char != 0) {
                bytesString[charCount] = char;
                charCount++;
            }
        }
        bytes memory bytesStringTrimmed = new bytes(charCount);
        for (uint j = 0; j < charCount; j++) {
            bytesStringTrimmed[j] = bytesString[j];
        }
        return string(bytesStringTrimmed);
    }
}