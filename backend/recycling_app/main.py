from fastapi import FastAPI
from recycling_app.api.routers import hello, waste_prediction

app = FastAPI()

app.router.include_router(hello.router)
app.router.include_router(waste_prediction.router)