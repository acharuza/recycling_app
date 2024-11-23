from fastapi import FastAPI
from recycling_app.api.routers import waste_prediction, user_feedback

app = FastAPI()

app.router.include_router(waste_prediction.router)
app.router.include_router(user_feedback.router)
