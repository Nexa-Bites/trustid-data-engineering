import os

paaword= "Hack#2025"

# Define the project structure
project_structure = {
    "data_ingestion": [
        "receive_verified_data.py",
        "receive_verified_credentials.py"
    ],
    "data_processing": [
        "clean_data.py",
        "transform_data.py",
        "encrypt_data.py"
    ],
    "storage": [
        "postgres_models.py",
        "indy_ledger.py",
        "openssl_keys.py"
    ],
    "integration": [
        "backend_api.py",
        "indy_api.py",
        "analytics_api.py"
    ],
    "config": [
        "settings.py",
        "database.py"
    ],
    "scripts": [
        "setup_db.py",
        "setup_indy.py"
    ],
    "tests": [
        "test_data_pipeline.py"
    ],
    "ocr_pipeline": [
        "README.md",
        "ocr_pipeline.py",
        "requirements.txt"
    ]
}

# Root-level files
root_files = [
    "Dockerfile",
    "docker-compose.yml",
    ".dockerignore",
    "Makefile",
    "requirements.txt",
    "README.md"
]

def create_project_structure():
    """Creates the entire project directory and files."""
    for folder, files in project_structure.items():
        os.makedirs(folder, exist_ok=True)
        for file in files:
            open(os.path.join(folder, file), 'w').close()
    
    # Create root-level files
    for file in root_files:
        open(file, 'w').close()

if __name__ == "__main__":
    create_project_structure()
    print("Project structure created successfully.")
