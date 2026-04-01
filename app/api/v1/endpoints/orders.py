from fastapi import APIRouter, HTTPException
from app.schemas.order import Order
from app.core.database import menu_db, orders_history

router = APIRouter()

@router.post("/")
def create_order(item_id: int, quantity: int = 1):
    item = next((i for i in menu_db if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món này!")
    
    new_order = Order(
        order_id=len(orders_history) + 1,
        item_name=item['name'],
        quantity=quantity,
        total_price=item['price'] * quantity
    )
    orders_history.append(new_order)
    return {"message": "Đặt món thành công", "order": new_order}

@router.get("/")
def get_all_orders():
    return orders_history