import json
import os
from indy import wallet, did
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
    (issuer_did, issuer_key) = await did.create_and_store_my_did(wallet_handle, "{}")

    # Close the wallet
    await wallet.close_wallet(wallet_handle)

    # Print the generated keys for debugging
    print("✅ Generated Indy Keys:")
    print(f"INDY_WALLET_ID=trustid_wallet")
    print(f"INDY_WALLET_KEY=trustid_secure_key")
    print(f"ISSUER_DID={issuer_did}")
    print(f"ISSUER_KEY={issuer_key}")

    # Update the .env file directly
    env_file = ".env"
    env_data = {}

    # Load existing .env content if it exists
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_data[key] = value

    # Update environment variables with generated keys
    env_data["INDY_WALLET_ID"] = "trustid_wallet"
    env_data["INDY_WALLET_KEY"] = "trustid_secure_key"
    env_data["ISSUER_DID"] = issuer_did
    env_data["ISSUER_KEY"] = issuer_key

    # Write updated content back to .env file
    with open(env_file, "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")

    print("✅ Indy keys generated and written directly to `.env`!")

# Run the async function
if __name__ == "__main__":
    asyncio.run(generate_keys())