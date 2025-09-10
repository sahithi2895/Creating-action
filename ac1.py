from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Optional
import random
from datetime import datetime, timedelta

# -------------------------------
# Initialize FastAPI
# -------------------------------
app = FastAPI(title="Grocery Bot Actions")

# -------------------------------
# Sample Data
# -------------------------------
AVAILABLE_ITEMS = {
    "Fruits": ["Apple", "Banana", "Orange", "Mango"],
    "Vegetables": ["Tomato", "Potato", "Carrot", "Spinach"],
    "Dairy": ["Milk", "Cheese", "Butter", "Yogurt"],
    "Beverages": ["Tea", "Coffee", "Juice", "Soda"]
}

INVENTORY = {
    "Apple": 50, "Banana": 100, "Orange": 80, "Mango": 30,
    "Tomato": 100, "Potato": 150, "Carrot": 70, "Spinach": 60,
    "Milk": 200, "Cheese": 50, "Butter": 40, "Yogurt": 100,
    "Tea": 80, "Coffee": 60, "Juice": 90, "Soda": 120
}

DISCOUNTS = {
    "SAVE10": 0.10,  # 10% discount
    "SAVE20": 0.20   # 20% discount
}

CARTS: Dict[str, Dict[str, int]] = {}  # Example: {"user1": {"Apple": 2, "Milk": 1}}

# -------------------------------
# Pydantic Models
# -------------------------------
class CategorySelection(BaseModel):
    category: str
    user_id: str

class ItemSelection(BaseModel):
    user_id: str
    items: Dict[str, int]  # item_name: quantity

class DiscountCode(BaseModel):
    user_id: str
    code: Optional[str] = None

class DeliveryInfo(BaseModel):
    user_id: str
    address: str

# -------------------------------
# Action Node 1: Fetch Items
# -------------------------------
@app.post("/fetch-items/")
def fetch_items(data: CategorySelection):
    category = data.category
    if category not in AVAILABLE_ITEMS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return {
        "category": category,
        "items": AVAILABLE_ITEMS[category]
    }

# -------------------------------
# Action Node 2: Add to Cart / Calculate Total
# -------------------------------
@app.post("/add-to-cart/")
def add_to_cart(selection: ItemSelection):
    user_id = selection.user_id
    if user_id not in CARTS:
        CARTS[user_id] = {}
    for item, qty in selection.items.items():
        if item in INVENTORY:
            CARTS[user_id][item] = CARTS[user_id].get(item, 0) + qty
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item {item} not found in inventory"
            )
    # Calculate total assuming each item costs $10 for simplicity
    total_price = sum(qty * 10 for qty in CARTS[user_id].values())
    return {"user_id": user_id, "cart": CARTS[user_id], "total_price": total_price}

# -------------------------------
# Action Node 3: Check Inventory
# -------------------------------
@app.post("/check-inventory/")
def check_inventory(selection: ItemSelection):
    unavailable_items = {}
    for item, qty in selection.items.items():
        stock = INVENTORY.get(item, 0)
        if qty > stock:
            unavailable_items[item] = {"requested": qty, "available": stock}
    if unavailable_items:
        return {"status": "some items unavailable", "details": unavailable_items}
    return {"status": "all items available"}

# -------------------------------
# Action Node 4: Apply Discounts / Coupons
# -------------------------------
@app.post("/apply-discount/")
def apply_discount(discount: DiscountCode):
    user_id = discount.user_id
    if user_id not in CARTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found for user"
        )
    total_price = sum(qty * 10 for qty in CARTS[user_id].values())
    if discount.code and discount.code in DISCOUNTS:
        discount_amount = total_price * DISCOUNTS[discount.code]
        total_price -= discount_amount
        return {"user_id": user_id, "cart": CARTS[user_id], "discount_code": discount.code, "total_price": total_price}
    return {"user_id": user_id, "cart": CARTS[user_id], "total_price": total_price, "message": "No valid discount applied"}

# -------------------------------
# Action Node 5: Place Order / Submit to Backend
# -------------------------------
@app.post("/place-order/")
def place_order(delivery: DeliveryInfo):
    user_id = delivery.user_id
    if user_id not in CARTS or not CARTS[user_id]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty or not found"
        )
    order_id = random.randint(1000, 9999)
    estimated_delivery = (datetime.now() + timedelta(days=3)).strftime("%d-%m-%Y")
    order_details = {
        "user_id": user_id,
        "order_id": order_id,
        "cart": CARTS[user_id],
        "delivery_address": delivery.address,
        "estimated_delivery": estimated_delivery
    }
    # Clear cart after placing order
    CARTS[user_id] = {}
    return order_details
