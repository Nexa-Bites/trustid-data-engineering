# # Use Python 3.9 as the base image
# FROM python:3.9-bullseye

# # Set the working directory
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     curl \
#     libssl-dev \
#     libffi-dev \
#     libpq-dev \
#     libsodium-dev \
#     python3-pip \
#     software-properties-common \
#     gnupg2 \
#     apt-transport-https \
#     ca-certificates

# # Install Rust and Cargo (needed for libindy build)
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
#     && . $HOME/.cargo/env \
#     && echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

# # Now build libindy
# RUN mkdir -p /tmp/libindy && cd /tmp/libindy \
#     && curl -sL https://github.com/hyperledger/indy-sdk/archive/v1.16.0.tar.gz | tar xz \
#     && cd indy-sdk-1.16.0/libindy \
#     && apt-get install -y build-essential pkg-config cmake libzmq3-dev \
#     && $HOME/.cargo/bin/cargo build --release \
#     && cp target/release/libindy.so /usr/lib/ \
#     && cp target/release/libindy.a /usr/lib/ \
#     && mkdir -p /usr/include/indy \
#     && cp include/*.h /usr/include/indy/ \
#     && cd /tmp && rm -rf /tmp/libindy

# # Install PostgreSQL client
# RUN apt-get install -y postgresql-client

# # Install Python dependencies
# COPY requirements.txt . 
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project files
# COPY . .

# # Ensure wallet directory exists and is persisted
# RUN mkdir -p /app/wallet

# # Set permissions for entrypoint script
# RUN chmod +x /app/entrypoint.sh

# # Run the entrypoint script
# ENTRYPOINT ["/app/entrypoint.sh"]



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

# Install Rust and Cargo (needed for libindy build)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . $HOME/.cargo/env \
    && echo 'source $HOME/.cargo/env' >> $HOME/.bashrc

# Build libindy
RUN mkdir -p /tmp/libindy && cd /tmp/libindy \
    && curl -sL https://github.com/hyperledger/indy-sdk/archive/v1.16.0.tar.gz | tar xz \
    && cd indy-sdk-1.16.0/libindy \
    && apt-get install -y build-essential pkg-config cmake libzmq3-dev \
    && $HOME/.cargo/bin/cargo build --release \
    && cp target/release/libindy.so /usr/lib/ \
    && cp target/release/libindy.a /usr/lib/ \
    && mkdir -p /usr/include/indy \
    && cp include/*.h /usr/include/indy/ \
    && cd /tmp && rm -rf /tmp/libindy

# Install PostgreSQL client
RUN apt-get install -y postgresql-client

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure wallet and keys directories exist
RUN mkdir -p /app/wallet /app/keys

# Set permissions for entrypoint script
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]