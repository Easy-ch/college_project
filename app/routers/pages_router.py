from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
from utils import load_services


router = APIRouter()
templates = Jinja2Templates(directory='templates')


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    services = load_services()
    return templates.TemplateResponse("index.html", {"request": request, "services": services})


@router.get('/login')
async def get_login_page(request:Request):
    return  templates.TemplateResponse("login.html", {"request": request})


@router.get('/register')
async def get_register_page(request:Request):
    return templates.TemplateResponse('register.html', {"request": request})


@router.get('/services')
async def get_services_page(request:Request):
    return templates.TemplateResponse('services.html', {"request": request})


@router.get('/profile')
async def get_services_page(request:Request):
    return templates.TemplateResponse('profile.html', {"request": request})


@router.get('/logout')
async def logout_route(response: Response, request:Request):
    response.set_cookie(
        key="refresh_token",
        value="",  
        httponly=True,
        secure=False,   # Использовать True для HTTPS
        samesite="Strict", 
        max_age=0  
    )
    return {"message": f"loggout"}


@router.get('/auth/forgot-password')
async def forgot_password(request:Request):
     return templates.TemplateResponse('forgot_password.html', {"request": request})

@router.get('/auth/reset-password')
async def reset_password(request:Request,token:str):
      return templates.TemplateResponse('reset-password.html', {"request": request,'token':token})


