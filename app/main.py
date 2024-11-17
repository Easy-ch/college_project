from fastapi import FastAPI
from routers.routers import router as router_pages
from routers.auth_router import app2 as router_validate
import uvicorn
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router_pages)
app.include_router(router_validate)

app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')


origins = [
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["POST","GET","PUT","DELETE"],
    allow_headers=["Content-Type"],
)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)