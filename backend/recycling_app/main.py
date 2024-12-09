from fastapi import FastAPI
from recycling_app.api.routers import waste_prediction, user_feedback
from recycling_app.database.database_manager import DatabaseManager

app = FastAPI()
db_manager = DatabaseManager()

app.router.include_router(waste_prediction.router)
app.router.include_router(user_feedback.router)
