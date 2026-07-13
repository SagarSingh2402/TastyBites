from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models.cart import Cart
from app.schemas.cart import CartCreate
from app.models.menu import Menu

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# Add Item To Cart
# -------------------------------

@router.post("/add")
def add_to_cart(
     request: Request,
    cart: CartCreate,
    db: Session = Depends(get_db)
):

    # Temporary user id
    user_id = request.session.get("user_id")

    existing_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.menu_id == cart.menu_id
    ).first()

    if existing_item:

        existing_item.quantity += cart.quantity

        db.commit()

        db.refresh(existing_item)

        return {
            "message": "Quantity Updated",
            "cart": existing_item
        }

    new_item = Cart(
        user_id=user_id,
        menu_id=cart.menu_id,
        quantity=cart.quantity
    )

    db.add(new_item)

    db.commit()

    db.refresh(new_item)

    return {
        "message": "Item Added To Cart",
        "cart": new_item
    }


# -------------------------------
# View Cart
# -------------------------------


@router.get("/")
def get_cart( request: Request,
             db: Session = Depends(get_db)):

    user_id = request.session.get("user_id")

    cart_items = db.query(Cart, Menu).join(
        Menu,
        Cart.menu_id == Menu.id
    ).filter(
        Cart.user_id == user_id
    ).all()

    result = []

    for cart, menu in cart_items:

        result.append({

            "id": cart.id,

            "menu_id": menu.id,

            "item_name": menu.item_name,

            "description": menu.description,

            "price": menu.price,

            "image": menu.image,

            "quantity": cart.quantity

        })

    return result

@router.put("/increase/{cart_id}")
def increase(cart_id: int, db: Session = Depends(get_db)):

    item = db.query(Cart).filter(
        Cart.id == cart_id
    ).first()

    if item:

        item.quantity += 1

        db.commit()

    return {"message":"Quantity Increased"}


@router.put("/decrease/{cart_id}")
def decrease(cart_id: int, db: Session = Depends(get_db)):

    item = db.query(Cart).filter(
        Cart.id == cart_id
    ).first()

    if item:

        if item.quantity > 1:

            item.quantity -= 1

            db.commit()

    return {"message":"Quantity Decreased"}

# -------------------------------
# Delete Item
# -------------------------------

@router.delete("/{cart_id}")
def delete_item(
    cart_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(Cart).filter(
        Cart.id == cart_id
    ).first()

    if not item:

        return {
            "message": "Item Not Found"
        }

    db.delete(item)

    db.commit()

    return {
        "message": "Item Deleted"
    }


@router.get("/page")
def cart_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="cart.html"
    )