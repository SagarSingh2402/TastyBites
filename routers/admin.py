
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

from app.database import SessionLocal
from app.models.order import Order
from app.models.user import User
from app.models.menu import Menu
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.schemas.menu import MenuCreate

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

templates = Jinja2Templates(directory="app/templates")

class StatusUpdate(BaseModel):
    status: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def admin_dashboard(request: Request):

    if request.session.get("role") != "admin":

        return templates.TemplateResponse(
            request=request,
            name="access_denied.html",
            context={
                "request": request,
                "message": "Only Admin Can Access This Page!"
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="admin.html"
    )


@router.get("/orders")
def all_orders(
    db: Session = Depends(get_db)
):
    orders = db.query(Order).order_by(
        Order.id.desc()
    ).all()

    return orders

@router.get("/stats")
def dashboard_stats(db: Session = Depends(get_db)):

    total_orders = db.query(Order).count()

    total_users = db.query(User).count()

    total_menu = db.query(Menu).count()

    revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    if revenue is None:
        revenue = 0

    return {
        "orders": total_orders,
        "users": total_users,
        "menu": total_menu,
        "revenue": revenue
    }

@router.get("/manage-orders")
def manage_orders(request: Request):

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/menu/")

    return templates.TemplateResponse(
        request=request,
        name="manage_orders.html"
    )

@router.put("/orders/{order_id}")
def update_order_status(
    order_id: int,
    data: StatusUpdate,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        return {
            "message": "Order Not Found"
        }

    order.status = data.status

    db.commit()

    db.refresh(order)

    return {
        "message": "Status Updated",
        "order": order
    }

@router.get("/menu")
def all_menu(
    db: Session = Depends(get_db)
):
    menu = db.query(Menu).all()
    return menu

@router.get("/manage-menu")
def manage_menu(request: Request):

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/menu/")

    return templates.TemplateResponse(
        request=request,
        name="manage_menu.html"
    )

@router.get("/add-menu")
def add_menu_page(request: Request):

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/menu/")

    return templates.TemplateResponse(
        request=request,
        name="add_menu.html"
    )
@router.post("/menu")
def add_menu_item(

    menu: MenuCreate,

    db: Session = Depends(get_db)

):

    new_item = Menu(

        item_name=menu.item_name,

        price=menu.price,

        category=menu.category,

        description=menu.description,

        image=menu.image

    )

    db.add(new_item)

    db.commit()

    db.refresh(new_item)

    return{

        "message":"Food Added Successfully"

    }

@router.get("/edit-menu/{menu_id}")
def edit_menu_page(
    menu_id:int,
    request:Request,
    db:Session=Depends(get_db)
):

    if request.session.get("role") != "admin":
        return RedirectResponse(url="/menu/")

    item = db.query(Menu).filter(
        Menu.id == menu_id
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="edit_menu.html",
        context={
            "request": request,
            "item": item
        }
    )

@router.put("/menu/{menu_id}")
def update_menu_item(
    menu_id: int,
    menu: MenuCreate,
    db: Session = Depends(get_db)
):

    item = db.query(Menu).filter(
        Menu.id == menu_id
    ).first()

    if not item:
        return {
            "message": "Menu Item Not Found"
        }

    item.item_name = menu.item_name
    item.price = menu.price
    item.category = menu.category
    item.description = menu.description
    item.image = menu.image

    db.commit()

    db.refresh(item)

    return {
        "message": "Menu Updated Successfully"
    }

@router.delete("/menu/{menu_id}")
def delete_menu_item(
    menu_id: int,
    db: Session = Depends(get_db)
):

    item = db.query(Menu).filter(
        Menu.id == menu_id
    ).first()

    if not item:
        return {
            "message": "Menu Item Not Found"
        }

    db.delete(item)

    db.commit()

    return {
        "message": "Menu Deleted Successfully"
    }