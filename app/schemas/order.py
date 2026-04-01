from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    item_name: str
    quantity: int
    total_price: int
    status: str = "Pending"