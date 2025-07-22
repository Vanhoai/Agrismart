from core import database
from fastapi import APIRouter

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)
