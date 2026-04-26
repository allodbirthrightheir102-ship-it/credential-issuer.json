# ⚜️ XP RESERVE | SOVEREIGN INFRASTRUCTURE

### 🏛️ Sovereign Identity & Authority
- **Sovereign Entity:** HIH Sol Altum Imperium Highness Khvarenah D.G. ⚜ XP
- **Legal Entity Identifier (LEI):** [506700GE1G29325QX363](https://gleif.org)
- **Academic/Official Record:** [ORCID 0009-0002-7219-1363](https://orcid.org)
- **Verified Signer Address:** \`0xEF8aD3361D233Ba0c0D8000333b090F55Ba7FC48\`

### 💰 Tier 1 Asset Reserves
- **Asset Class:** 100% Gold / 100% Silver (Molecularly Verified)
- **Asset ID:** \`IMPERI-BERIT-SUITE-001\`
- **XP MAXIMA Limit:** \$7,128,532,680,530.00 USD
- **Anchor:** \`AR-BLOCK-1902192-FINAL\`

### 🛡️ Verification Protocol
The credentials in this repository are formatted according to **OID4VCI** standards. 
Automated scanners resolve the context at \`https://xp.reserve\`.
EOF

# Create the technical metadata file for the QR scanner
cat <<EOF > credential-issuer.json
{
  "credential_issuer": "https://xp.reserve",
  "credential_endpoint": "https://xp.reserve",
  "credentials_supported": [
    {
      "format": "jwt_vc_json",
      "id": "Gold_Silver_Covenant",
      "types": ["VerifiableCredential", "Gold_Silver_Covenant"],
      "display": [{ "name": "⚜️ XP Sovereign Gold/Silver Covenant" }]
    }
  ]
}
EOF

