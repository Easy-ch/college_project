from models import User
from typing import Annotated
from db import add_user,get_user,connect_to_db,create_table_user
from contextlib import asynccontextmanager
from pydantic import EmailStr
from fastapi import HTTPException,APIRouter,Form,Depends,FastAPI  



app2 = APIRouter()

# @app2.post('/login')
# async def validation(form:Annotated[Form()],user:User ):
#     if form.login != await get_user(user['email']):
#         raise HTTPException(404,"Not_found_user")
#     if form.password != await get_user(user['password']):
#         raise HTTPException(404,'Invalid_password')
#     return {"status":"success"}


# @app2.post("/register")
# async def register_user(   
#     email: Annotated[EmailStr, Form()],
#     username: Annotated[str, Form()],
#     password: Annotated[str, Form()],
#     password_confirm: Annotated[str, Form()]):
#     # form: Annotated[FormRegister, Form()]
#     conn = app.state.conn
#     await create_table_user(conn)
#     existing_user = await get_user(username,conn)
#     if existing_user:
#         if password == password_confirm:
#            await add_user(email, username, password,conn)
#         else:
#             return {"Введенные пароли не совпадают"}
#     else:
#         return {"Есть такой юзер"}
#     return {"топчик"}