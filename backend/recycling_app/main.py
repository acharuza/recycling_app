from fastapi import FastAPI
from recycling_app.api.routers import waste_prediction, user_feedback
from recycling_app.database.database_manager import DatabaseManager
from recycling_app.model.model_manager import ModelManager
from recycling_app.constants import DATABASE_PATH

app = FastAPI()
db_manager = DatabaseManager(database_path=DATABASE_PATH)
model_manager = ModelManager()

app.router.include_router(waste_prediction.router)
app.router.include_router(user_feedback.router)
