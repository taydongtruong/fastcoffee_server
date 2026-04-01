from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Fast Coffee Professional Test")

# --- 1. Models (Khuôn mẫu dữ liệu) ---
class MenuItem(BaseModel):
    id: int
    name: str
    price: int

class UpdatePriceModel(BaseModel):
    price: int

class Order(BaseModel):
    order_id: int
    item_name: str
    quantity: int
    total_price: int
    status: str = "Pending" # Trạng thái: Pending, Done, Cancelled

# --- 2. Database giả lập (In-memory) ---
menu = [
    {"id": 1, "name": "Cà phê Đen", "price": 20000},
    {"id": 2, "name": "Cà phê Sữa", "price": 25000},
    {"id": 3, "name": "Bạc Xỉu", "price": 29000},
]

orders_history: List[Order] = []

# --- 3. Các API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Hệ thống Fast Coffee sẵn sàng!"}

# --- NHÓM MENU (QUẢN LÝ THỰC ĐƠN) ---

@app.get("/menu", tags=["Menu"])
def get_menu():
    """Xem danh sách thực đơn"""
    return menu

@app.post("/menu", tags=["Menu"])
def add_item(item: MenuItem):
    """Thêm món mới vào thực đơn"""
    if any(i["id"] == item.id for i in menu):
        raise HTTPException(status_code=400, detail="ID món đã tồn tại!")
    menu.append(item.dict())
    return {"message": "Thêm món thành công", "new_item": item}

@app.patch("/menu/{item_id}", tags=["Menu"])
def update_price(item_id: int, data: UpdatePriceModel):
    """Cập nhật giá tiền của một món (PATCH)"""
    item = next((i for i in menu if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món!")
    item["price"] = data.price
    return {"message": f"Đã cập nhật giá mới cho {item['name']}", "updated_item": item}

@app.delete("/menu/{item_id}", tags=["Menu"])
def delete_item(item_id: int):
    """Xóa một món khỏi thực đơn (DELETE)"""
    global menu
    item = next((i for i in menu if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món để xóa!")
    menu = [i for i in menu if i["id"] != item_id]
    return {"message": f"Đã xóa món {item['name']} khỏi thực đơn"}

# --- NHÓM ORDERS (QUẢN LÝ ĐƠN HÀNG) ---

@app.post("/order", tags=["Orders"])
def create_order(item_id: int, quantity: int = 1):
    """Đặt món và lưu vào lịch sử (POST)"""
    item = next((i for i in menu if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món này!")
    
    total = item["price"] * quantity
    new_order = Order(
        order_id=len(orders_history) + 1,
        item_name=item['name'],
        quantity=quantity,
        total_price=total
    )
    orders_history.append(new_order)
    return {"message": "Đặt món thành công", "order": new_order}

@app.get("/orders", tags=["Orders"])
def get_all_orders():
    """Xem lại toàn bộ lịch sử đơn hàng (GET)"""
    return orders_history

@app.patch("/orders/{order_id}/status", tags=["Orders"])
def update_order_status(order_id: int, status: str):
    """Cập nhật trạng thái đơn hàng: Pending -> Done (PATCH)"""
    order = next((o for o in orders_history if o.order_id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng!")
    order.status = status
    return {"message": "Cập nhật trạng thái thành công", "order": order}