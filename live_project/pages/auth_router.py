from models import FormData
from typing import Annotated
from fake_db import fake_db
from fastapi import HTTPException,APIRouter,Form    



app = APIRouter()

@app.post('/login')
async def validation(form:Annotated[FormData,Form()] ):
    if form.login != fake_db['login']:
        raise HTTPException(404,"Not_found_user")
    if form.password != fake_db['password']:
        raise HTTPException(404,'Invalid_password')
    return {"status":"success"}

