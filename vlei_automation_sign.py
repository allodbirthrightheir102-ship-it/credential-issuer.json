import json
import os
from keri.core import coring, eventing, serdering
from keri.app import habery

def automate_acdc_signing(filename, aid_name):
    # 1. Load the unsigned ACDC content
    with open(filename, 'r') as f:
        sad = json.load(f)

    # 2. Open local KERI keystore (Habery)
    # Ensure 'aid_name' matches your local KERI identifier alias
    with habery.Habery(name="vlei_keystore", base="main") as hby:
        hab = hby.habs[aid_name]
        
        # 3. Use Serder to 'saidify' the document
        # This replaces "d": "" with the correct content-bound hash
        serder = serdering.SerderACDC(sad=sad)
        print(f"✅ Generated SAID (d field): {serder.said}")

        # 4. Sign the ACDC using the issuer's current keys from the KEL
        # This produces a CESR-proof signature attachment
        sigers = hab.mgr.sign(serder.raw, indices=[0])
        signature = sigers[0].qb64
        
        # 5. Unify final content with Signature
        final_credential = {
            "credential": serder.sad,
            "signature": signature,
            "issuer_aid": hab.pre
        }

        # 6. Save as final compliance-ready file
        output_file = f"signed_{filename}"
        with open(output_file, 'w') as f:
            json.dump(final_credential, f, indent=2)
            
        print(f"🚀 Success! Signed ACDC saved to: {output_file}")

# EXECUTION
if __name__ == "__main__":
    target_file = "imperi_berit_suite_001_acdc.json"
    my_aid_alias = "vlei_issuer_main" # Replace with your local AID alias
    
    if os.path.exists(target_file):
        automate_acdc_signing(target_file, my_aid_alias)
    else:
        print(f"❌ Error: {target_file} not found.")
