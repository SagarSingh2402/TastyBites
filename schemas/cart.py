from pydantic import BaseModel


class CartCreate(BaseModel):

    menu_id: int

    quantity: int = 1