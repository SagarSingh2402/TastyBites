from pydantic import BaseModel


class OrderCreate(BaseModel):

    customer_name: str

    phone: str

    address: str

    payment_method: str