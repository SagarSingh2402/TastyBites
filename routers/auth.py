from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse  

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Register Page
# -----------------------------

@router.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )
# -----------------------------
# Login Page
# -----------------------------

@router.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

# -----------------------------
# Register API
# -----------------------------
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email Already Registered"
        }

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User Registered Successfully"
    }


# -----------------------------
# Login API
# -----------------------------
@router.post("/login")
def login(
    request: Request,
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email,
        User.password == user.password
    ).first()

    if not existing_user:
        return {
            "message": "Invalid Email or Password"
        }

    # Session Save
    request.session["user_id"] = existing_user.id
    request.session["role"] = existing_user.role

    if existing_user.role == "admin":
        return {
            "message": "Admin Login",
            "redirect": "/admin"
        }

    return {
        "message": "Customer Login",
        "redirect": "/menu/"
    }

