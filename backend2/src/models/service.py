from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, CheckConstraint
from src.models.base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    duration_quarters = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    master_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        CheckConstraint("duration_quarters > 0", name="check_duration_positive"),
        CheckConstraint("price > 0", name="check_price_positive"),
    )



