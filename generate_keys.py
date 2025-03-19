# import json
# import os
# import asyncio
# from indy import wallet, did
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Wallet Storage Configuration
# WALLET_STORAGE_PATH = "/app/wallet"  # Persistent location inside container

# # Ensure the wallet directory exists
# os.makedirs(WALLET_STORAGE_PATH, exist_ok=True)

# WALLET_CONFIG = json.dumps({
#     "id": "trustid_wallet",
#     "storage_type": "default",
#     "storage_config": {"path": WALLET_STORAGE_PATH}
# })
# WALLET_CREDENTIALS = json.dumps({"key": "trustid_secure_key"})


# async def wallet_exists():
#     """Check if the Indy wallet already exists before creating it."""
#     try:
#         wallet_handle = await wallet.open_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)
#         await wallet.close_wallet(wallet_handle)
#         return True
#     except Exception as e:
#         print(f"⚠️ Wallet check failed: {e}")
#         return False


# async def generate_keys():
#     """Generate and store Indy DID keys."""
#     try:
#         if not await wallet_exists():
#             try:
#                 print("🚀 Creating new wallet...")
#                 await wallet.create_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)
#                 print("✅ Wallet created successfully.")
#             except Exception as e:
#                 print(f"⚠️ Wallet creation failed: {e}")
#                 return 1

#         # Open wallet
#         print("🔑 Opening wallet...")
#         wallet_handle = await wallet.open_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)

#         # Generate a new DID
#         print("🔐 Generating DID and keys...")
#         issuer_did, issuer_key = await did.create_and_store_my_did(wallet_handle, "{}")

#         # Close wallet
#         await wallet.close_wallet(wallet_handle)

#         print("✅ Generated Indy Keys:")
#         print(f"INDY_WALLET_ID=trustid_wallet")
#         print(f"INDY_WALLET_KEY=trustid_secure_key")
#         print(f"ISSUER_DID={issuer_did}")
#         print(f"ISSUER_KEY={issuer_key}")

#         # Update .env file
#         update_env_file(issuer_did, issuer_key)

#         print("✅ Key generation completed successfully!")
#         return 0
#     except Exception as e:
#         print(f"❌ Key generation failed: {e}")
#         return 1


# def update_env_file(issuer_did, issuer_key):
#     """Update the .env file with generated Indy keys."""
#     env_file = "/app/.env"  # Ensure the correct path to the .env file
#     env_data = {}

#     # Read existing .env file if it exists
#     if os.path.exists(env_file):
#         with open(env_file, "r") as f:
#             for line in f:
#                 if "=" in line:
#                     key, value = line.strip().split("=", 1)
#                     env_data[key] = value

#     # Update with new keys
#     env_data["INDY_WALLET_ID"] = "trustid_wallet"
#     env_data["INDY_WALLET_KEY"] = "trustid_secure_key"
#     env_data["ISSUER_DID"] = issuer_did
#     env_data["ISSUER_KEY"] = issuer_key

#     # Write updated .env file
#     with open(env_file, "w") as f:
#         for key, value in env_data.items():
#             f.write(f"{key}={value}\n")

#     print(f"✅ Indy keys written to `{env_file}`!")


# if __name__ == "__main__":
#     exit_code = asyncio.run(generate_keys())
#     exit(exit_code)



import json
import os
import asyncio
from indy import wallet, did
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Wallet Storage Configuration
WALLET_STORAGE_PATH = "/app/wallet"  # Persistent location inside container

# Ensure the wallet directory exists
os.makedirs(WALLET_STORAGE_PATH, exist_ok=True)

WALLET_CONFIG = json.dumps({
    "id": "trustid_wallet",
    "storage_type": "default",
    "storage_config": {"path": WALLET_STORAGE_PATH}
})
WALLET_CREDENTIALS = json.dumps({"key": "trustid_secure_key"})


async def wallet_exists():
    """Check if the Indy wallet already exists before creating it."""
    try:
        wallet_handle = await wallet.open_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)
        await wallet.close_wallet(wallet_handle)
        return True
    except Exception as e:
        print(f"⚠️ Wallet check failed: {e}")
        return False


async def generate_keys():
    """Generate and store Indy DID keys."""
    try:
        if not await wallet_exists():
            try:
                print("🚀 Creating new wallet...")
                await wallet.create_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)
                print("✅ Wallet created successfully.")
            except Exception as e:
                print(f"⚠️ Wallet creation failed: {e}")
                return 1

        # Open wallet
        print("🔑 Opening wallet...")
        wallet_handle = await wallet.open_wallet(WALLET_CONFIG, WALLET_CREDENTIALS)

        # Generate a new DID
        print("🔐 Generating DID and keys...")
        issuer_did, issuer_key = await did.create_and_store_my_did(wallet_handle, "{}")

        # Close wallet
        await wallet.close_wallet(wallet_handle)

        print("✅ Generated Indy Keys:")
        print(f"INDY_WALLET_ID=trustid_wallet")
        print(f"INDY_WALLET_KEY=trustid_secure_key")
        print(f"ISSUER_DID={issuer_did}")
        print(f"ISSUER_KEY={issuer_key}")

        # Update .env file
        update_env_file(issuer_did, issuer_key)

        # Save keys to JSON file
        save_keys_to_json(issuer_did, issuer_key)

        print("✅ Key generation completed successfully!")
        return 0
    except Exception as e:
        print(f"❌ Key generation failed: {e}")
        return 1


def update_env_file(issuer_did, issuer_key):
    """Update the .env file with generated Indy keys."""
    env_file = "/app/.env"  # Ensure the correct path to the .env file
    env_data = {}

    # Read existing .env file if it exists
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    env_data[key] = value

    # Update with new keys
    env_data["INDY_WALLET_ID"] = "trustid_wallet"
    env_data["INDY_WALLET_KEY"] = "trustid_secure_key"
    env_data["ISSUER_DID"] = issuer_did
    env_data["ISSUER_KEY"] = issuer_key

    # Write updated .env file
    with open(env_file, "w") as f:
        for key, value in env_data.items():
            f.write(f"{key}={value}\n")

    print(f"✅ Indy keys written to `{env_file}`!")


def save_keys_to_json(issuer_did, issuer_key):
    """Save generated keys to a JSON file."""
    keys_dir = "/app/keys"
    keys_file = os.path.join(keys_dir, "my_keys.json")
    
    os.makedirs(keys_dir, exist_ok=True)
    
    keys_data = {
        "issuer_did": issuer_did,
        "issuer_key": issuer_key
    }
    
    with open(keys_file, "w") as f:
        json.dump(keys_data, f)
    
    print(f"✅ Keys saved to `{keys_file}`!")


if __name__ == "__main__":
    exit_code = asyncio.run(generate_keys())
    exit(exit_code)