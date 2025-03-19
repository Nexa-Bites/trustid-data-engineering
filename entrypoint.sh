#!/bin/bash
set -e

KEYS_DIR="/app/keys"
KEY_FILE="$KEYS_DIR/my_keys.json"

# Ensure the keys directory exists
mkdir -p "$KEYS_DIR"

# Check if keys already exist before generating new ones
if [ -f "$KEY_FILE" ]; then
    echo "Keys already exist. Skipping generation."
else
    echo "Generating new keys..."
    python generate_keys.py
fi

# Run the CMD from Dockerfile
exec "$@"
