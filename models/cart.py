from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Cart(Base):

    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    menu_id = Column(Integer, ForeignKey("menu.id"))

    quantity = Column(Integer, default=1)

    # Relationships
    user = relationship("User")
    menu = relationship("Menu")