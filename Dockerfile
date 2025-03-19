# Use a full Debian-based Python image instead of slim for better compatibility
FROM python:3.9-bullseye

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install the Indy SDK manually
RUN curl -L https://github.com/hyperledger/indy-sdk/releases/download/v1.16.0/libindy_1.16.0_ubuntu_20.04.deb -o libindy.deb && \
    dpkg -i libindy.deb || apt-get install -f -y && \
    rm libindy.deb

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for storing generated keys
RUN mkdir -p /app/keys

# Copy the entire project
COPY . .

# Ensure the entrypoint script is executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command (will be executed after entrypoint)
CMD ["python", "generate_keys.py"]
