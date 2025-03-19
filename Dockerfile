version: "3.8"

services:
  postgres:
    image: postgres:13
    restart: always  # Ensures Postgres restarts on failure
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: trustid
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    restart: always  # Ensures app restarts if it crashes
    depends_on:
      - postgres
    environment:
      POSTGRES_URL: "postgresql://user:password@postgres:5432/trustid"
    ports:
      - "8000:8000"
    volumes:
      - ./docker/entrypoint.sh:/app/docker/entrypoint.sh  # Ensure entrypoint.sh is mounted
    entrypoint: ["/bin/sh", "/app/docker/entrypoint.sh"]  # Explicitly define entrypoint

volumes:
  postgres_data:
