from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    user_id: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    email: str = Field(encrypted=True)
    phone_number: Optional[str] = Field(encrypted=True)
    dob: datetime.date = Field(encrypted=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    dids: List["DID"] = Relationship(back_populates="user")
    credentials: List["Credential"] = Relationship(back_populates="user")
    consents: List["Consent"] = Relationship(back_populates="user")

class DID(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    did_id: str = Field(unique=True, index=True)
    user_id: str = Field(foreign_key="user.user_id")
    public_key: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional[User] = Relationship(back_populates="dids")

class Schema(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    schema_id: str = Field(unique=True, index=True)
    schema_name: str
    attributes: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CredentialDefinition(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    cred_def_id: str = Field(unique=True, index=True)
    schema_id: str = Field(foreign_key="schema.schema_id")
    issuer_did: str
    signature_type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Credential(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    credential_id: str = Field(unique=True, index=True)
    cred_def_id: str = Field(foreign_key="credentialdefinition.cred_def_id")
    user_id: str = Field(foreign_key="user.user_id")
    attributes: str  # Encrypted credential data
    status: str = Field(default="Active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional[User] = Relationship(back_populates="credentials")

class RevocationRegistry(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    revocation_id: str = Field(unique=True, index=True)
    credential_id: str = Field(foreign_key="credential.credential_id")
    revoked_at: datetime = Field(default_factory=datetime.utcnow)

class Consent(SQLModel, table=True):  # Added for GDPR/CCPA compliance
    id: int = Field(primary_key=True, index=True)
    consent_id: str = Field(unique=True, index=True)
    user_id: str = Field(foreign_key="user.user_id")
    purpose: str  # e.g., "Data Processing", "Credential Issuance"
    granted: bool = Field(default=False)
    granted_at: Optional[datetime] = Field(default=None)
    expires_at: Optional[datetime] = Field(default=None)  # Retention policy
    user: Optional[User] = Relationship(back_populates="consents")
    # Note: Retention policy to delete expired consents can be implemented in a cron job
