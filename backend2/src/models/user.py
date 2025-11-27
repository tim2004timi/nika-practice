from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.sql import func
from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    role = Column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "role IN ('CLIENT', 'VIZAZHIST', 'MANICURIST', 'STYLIST', 'BROWIST')",
            name="check_user_role"
        ),
    )



