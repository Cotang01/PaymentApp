from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(20))
    second_name: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
        )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    
    def __repr__(self):
        return f"User(first_name={self.first_name}, \
                 second_name={self.second_name}, \
                 email={self.email}), \
                 is_superuser={self.is_superuser}"