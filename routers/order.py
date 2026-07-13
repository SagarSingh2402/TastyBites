from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models.order import Order
from app.models.cart import Cart
from app.models.menu import Menu
from app.schemas.order import OrderCreate
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/order",
    tags=["Order"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Place Order
# -----------------------------
@router.get("/page")
def order_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="orders.html"
    )

@router.get("/history/data")
def order_history(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    orders = db.query(Order).filter(
        Order.user_id == user_id
    ).order_by(Order.id.desc()).all()

    return orders

@router.get("/history")
def history_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="orders.html"
    )

@router.get("/checkout")
def checkout_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="checkout.html"
    )

@router.post("/place")
def place_order(
    request: Request,
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    cart_items = db.query(Cart, Menu).join(
        Menu,
        Cart.menu_id == Menu.id
    ).filter(
        Cart.user_id == user_id
    ).all()

    if len(cart_items) == 0:

        return {
            "message": "Cart is Empty"
        }

    total = 0

    for cart, menu in cart_items:

        total += menu.price * cart.quantity

    new_order = Order(

        user_id=user_id,

        customer_name=order.customer_name,

        phone=order.phone,

        address=order.address,

        payment_method=order.payment_method,

        total_amount=total,

        status="Pending"

    )

    db.add(new_order)

    db.commit()

    db.refresh(new_order)

    # Empty Cart

    db.query(Cart).filter(
        Cart.user_id == user_id
    ).delete()

    db.commit()

    return {

        "message": "Order Placed Successfully",

        "order_id": new_order.id,

        "total": total

    }

@router.get("/success")
def order_success(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="order_success.html"
    )


