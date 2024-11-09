from fastapi import FastAPI
from recycling_app.api.routers import hello 

app = FastAPI()

app.router.include_router(hello.router)