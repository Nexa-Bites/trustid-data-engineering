# Use Python 3.9 as the base image
FROM python:3.9-bullseye

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    libsodium-dev \
    python3-pip \
    software-properties-common \
    gnupg2 \
    apt-transport-https \
    ca-certificates

# Fix the Sovrin repository configuration
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 68DB5E88 \
    && echo "deb https://repo.sovrin.org/sdk/deb bionic stable" > /etc/apt/sources.list.d/sovrin.list \
    && apt-get update \
    && apt-get install -y libindy

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set permissions for entrypoint
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]