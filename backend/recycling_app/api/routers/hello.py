from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def read_hello(name: str = "World"):
    return {"Hello": name}