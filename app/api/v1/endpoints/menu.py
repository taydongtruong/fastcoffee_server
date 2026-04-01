from fastapi import APIRouter, HTTPException
from app.schemas.menu import MenuItem, UpdatePriceModel
from app.core.database import menu_db

router = APIRouter()

@router.get("/")
def get_menu():
    return menu_db

@router.post("/")
def add_item(item: MenuItem):
    if any(i["id"] == item.id for i in menu_db):
        raise HTTPException(status_code=400, detail="ID món đã tồn tại!")
    menu_db.append(item.dict())
    return {"message": "Thêm món thành công", "new_item": item}

@router.patch("/{item_id}")
def update_price(item_id: int, data: UpdatePriceModel):
    item = next((i for i in menu_db if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món!")
    item["price"] = data.price
    return {"message": "Cập nhật thành công", "updated_item": item}

@router.delete("/{item_id}")
def delete_item(item_id: int):
    global menu_db
    item = next((i for i in menu_db if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món!")
    menu_db[:] = [i for i in menu_db if i["id"] != item_id] # Xóa trực tiếp trong list
    return {"message": f"Đã xóa {item['name']}"}