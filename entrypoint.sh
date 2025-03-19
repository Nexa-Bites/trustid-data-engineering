# #!/bin/bash
# set -e

# KEYS_DIR="/app/keys"
# KEY_FILE="$KEYS_DIR/my_keys.json"
# ENV_FILE="/app/.env"

# # Ensure the keys directory exists
# mkdir -p "$KEYS_DIR"

# # Load existing keys if available
# if [ -f "$KEY_FILE" ]; then
#     echo "✅ Indy keys already exist. Loading from file..."

#     # Extract keys from JSON file
#     ISSUER_DID=$(jq -r '.issuer_did' "$KEY_FILE")
#     ISSUER_KEY=$(jq -r '.issuer_key' "$KEY_FILE")

#     # Ensure the environment file is updated
#     echo "INDY_WALLET_ID=trustid_wallet" > "$ENV_FILE"
#     echo "INDY_WALLET_KEY=trustid_secure_key" >> "$ENV_FILE"
#     echo "ISSUER_DID=$ISSUER_DID" >> "$ENV_FILE"
#     echo "ISSUER_KEY=$ISSUER_KEY" >> "$ENV_FILE"

#     echo "✅ Loaded existing keys into environment variables."
# else
#     echo "🚀 No keys found, generating new ones..."
#     python generate_keys.py

#     # Ensure keys are saved in the volume for persistence
#     if [ -f "$KEY_FILE" ]; then
#         echo "✅ New keys successfully generated and stored."
#     else
#         echo "❌ Key generation failed!"
#         exit 1
#     fi
# fi

# # Start the application
# exec "$@"


#!/bin/bash
set -e

KEYS_DIR="/app/keys"
KEY_FILE="$KEYS_DIR/my_keys.json"
ENV_FILE="/app/.env"

# Ensure the keys directory exists
mkdir -p "$KEYS_DIR"

# Check if keys already exist in .env
if grep -q "ISSUER_DID" "$ENV_FILE" && grep -q "ISSUER_KEY" "$ENV_FILE"; then
    echo "✅ Indy keys already exist in .env."
else
    echo "🚀 No keys found, generating new ones..."
    python generate_keys.py

    # Verify keys were written to .env
    if grep -q "ISSUER_DID" "$ENV_FILE" && grep -q "ISSUER_KEY" "$ENV_FILE"; then
        echo "✅ New keys successfully generated and stored in .env."
    else
        echo "❌ Key generation failed!"
        exit 1
    fi
fi

# Start the application
exec "$@"