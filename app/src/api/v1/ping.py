from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from http import HTTPStatus

from src.db.mongo import get_mongo_db

router = APIRouter()


@router.get("/", status_code=200)
async def ping():
    """
    Эндпоинт для проверки работы сервера
    """
    return {"status": "ok", "message": "Server is up and running."}


@router.get("/mongo", status_code=200)
async def health_check(mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    """
    Эндпоинт для проверки состояния MongoDB
    """
    try:
        ping_result = await mongo_db.command("ping")
        if not ping_result.get("ok"):
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail="MongoDB not available"
            )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}",
        )
    return {"status": "ok", "message": "All systems operational"}