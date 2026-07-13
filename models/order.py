from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    customer_name = Column(String(100))

    phone = Column(String(20))

    address = Column(String(255))

    payment_method = Column(String(50))

    total_amount = Column(Integer)

    status = Column(String(50), default="Pending")

    created_at = Column(DateTime, default=datetime.utcnow)