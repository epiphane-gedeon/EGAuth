import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")
    authorization_codes: Mapped[list["AuthorizationCode"]] = relationship(
        back_populates="user"
    )


class OAuthClient(Base):
    __tablename__ = "clients"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_id: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    client_secret_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    redirect_uris: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    allowed_scopes: Mapped[list[str]] = mapped_column(
        ARRAY(Text), default=["openid", "profile", "email"]
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )


class AuthorizationCode(Base):
    __tablename__ = "authorization_codes"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    client_id: Mapped[str] = mapped_column(String(100))
    redirect_uri: Mapped[str] = mapped_column(Text)
    scopes: Mapped[list[str]] = mapped_column(ARRAY(Text))
    code_challenge: Mapped[str | None] = mapped_column(String(255))  # PKCE
    code_challenge_method: Mapped[str | None] = mapped_column(String(10))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped["User"] = relationship(back_populates="authorization_codes")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    token: Mapped[str] = mapped_column(String(512), unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    client_id: Mapped[str] = mapped_column(String(100))
    scopes: Mapped[list[str]] = mapped_column(ARRAY(Text))
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    user: Mapped["User"] = relationship(back_populates="refresh_tokens")
