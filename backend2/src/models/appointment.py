from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, CheckConstraint
from src.models.base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    quarter = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="booked")
    is_paid = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("quarter >= 1 AND quarter <= 20", name="check_quarter_range"),
        CheckConstraint(
            "status IN ('booked', 'in_progress', 'completed')",
            name="check_appointment_status"
        ),
    )

