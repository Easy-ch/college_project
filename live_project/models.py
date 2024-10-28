from pydantic import BaseModel



class FormData(BaseModel):
    login: str 
    password : str 
