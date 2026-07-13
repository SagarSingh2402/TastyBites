from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


from app.database import Base, engine

# Routers
from app.routers import menu as menu_router
from app.routers import auth as auth_router
from app.routers import cart as cart_router

# Models
from app.routers import order as order_router
from app.models import user
from app.models import menu
from app.models import cart
from app.routers import admin

app = FastAPI(
    title="Restaurant Management System",
    description="Restaurant Menu Project"
)
app.add_middleware(
    SessionMiddleware,
    secret_key="restaurant_secret_key_123"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(menu_router.router)
app.include_router(auth_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
app.include_router(admin.router)

@app.get("/")
def home():

    return RedirectResponse(url="/auth/login")

#rom fastapi import APIRouter, Request
#rom fastapi.templating import Jinja2Templates

#outer = APIRouter(prefix="/menu", tags=["menu"])

#emplates = Jinja2Templates(directory="app/templates")

#router.get("/")
#ef home(request: Request):
#   return templates.TemplateResponse(
#       "index.html",
#       {"request": request}
#   )