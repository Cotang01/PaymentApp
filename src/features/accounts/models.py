from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    last_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
        )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False
        )
    is_superuser: Mapped[bool] = mapped_column(default=False)
    
    def __repr__(self):
        return f"User(first_name={self.first_name}" \
               f"last_name={self.last_name}" \
               f"email={self.email})" \
               f"is_superuser={self.is_superuser}" \


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
        )
    token_hash: Mapped[str] = mapped_column(
        String(255), index=True, unique=True
        )
    exp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
        )
    abs_exp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
        )
    iat: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=datetime.now(UTC)
                                          )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
        )
    ip: Mapped[str | None] = mapped_column(
        String(15), nullable=True, default=None
        )
    user_agent: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
        )

    def __repr__(self):
        return f"RefreshToken(user_id={self.user_id}" \
               f"token_hash={self.token_hash}" \
               f"exp={self.exp}" \
               f"abs_exp={self.abs_exp}" \
               f"iat={self.iat}" \
               f"revoked_at={self.revoked_at}" \
               f"ip={self.ip}" \
               f"user_agent={self.user_agent})"
