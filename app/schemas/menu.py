from pydantic import BaseModel

class MenuItem(BaseModel):
    id: int
    name: str
    price: int

class UpdatePriceModel(BaseModel):
    price: int