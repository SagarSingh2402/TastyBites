from pydantic import BaseModel

class MenuCreate(BaseModel):
    item_name: str
    price: int
    image: str
    category: str
    description: str



class MenuResponse(BaseModel):

    id:int

    item_name:str

    price:int

    image:str

    category:str

    description:str

    class Config:

        from_attributes=True
