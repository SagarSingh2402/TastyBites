from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.menu import Menu

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)

templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="menu.html"
    )


@router.get("/items")
def get_menu(db: Session = Depends(get_db)):

    menu = db.query(Menu).all()

    return menu