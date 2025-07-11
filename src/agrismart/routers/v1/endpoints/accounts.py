from core import database
from fastapi import APIRouter

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@router.get("/")
async def get_accounts():
    collections = await database.collections()
    print(f"Available collections: {collections}")
    return {"message": "List of accounts"}
