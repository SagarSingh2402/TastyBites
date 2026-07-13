from sqlalchemy import Column,Integer,String

from app.database import Base


class Menu(Base):

    __tablename__="menu"

    id=Column(Integer,primary_key=True,index=True)

    item_name=Column(String)

    price=Column(Integer)

    image=Column(String)

    category=Column(String)

    description=Column(String)    