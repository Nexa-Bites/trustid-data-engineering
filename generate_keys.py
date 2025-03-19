import json
import os
from indy import wallet
import asyncio

# Define wallet credentials
WALLET_CONFIG = json.dumps({"id": "trustid_wallet"})
WALLET_CREDENTIALS = json.dumps({"key": "trustid_secure_key"})

async def generate_keys():
    try:
        # Create the wallet (if it doesn't exist)
        await wallet.create_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)
    except Exception as e:
        print(f"Wallet might already exist: {e}")

    # Open the wallet
    wallet_handle = await wallet.open_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)

    # Generate a new DID (Decentralized Identifier)
    (issuer_did, issuer_key) = await wallet.create_and_store_my_did(wallet_handle, "{}")

    # Close the wallet
    await wallet.close_wallet(wallet_handle)

    # Save the keys to a file
    with open("indy_keys.txt", "w") as f:
        f.write(f"INDY_WALLET_ID=trustid_wallet\n")
        f.write(f"INDY_WALLET_KEY=trustid_secure_key\n")
        f.write(f"ISSUER_DID={issuer_did}\n")
        f.write(f"ISSUER_KEY={issuer_key}\n")

    print("✅ Indy keys generated and saved to `indy_keys.txt`. Copy them to `.env`!")

# Run the async function
if __name__ == "__main__":
    asyncio.run(generate_keys())
