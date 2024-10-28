from fastapi import Request,APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get('/login')
def get_login_page(request:Request):
    return  templates.TemplateResponse("login.html",{"request":request})



