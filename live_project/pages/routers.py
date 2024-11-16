from fastapi import Request,APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get('/login')
async def get_login_page(request:Request):
    return  templates.TemplateResponse("login.html",{"request":request})


@router.get('/register')
async def get_register_page(request:Request):
    return templates.TemplateResponse('register.html',{"request":request})


@router.get('/services')
async def get_services_page(request:Request):
    return templates.TemplateResponse('services.html',{"request":request})


