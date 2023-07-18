from fastapi import APIRouter

from src.api.endpoints.api_methods import router

api_router = APIRouter()
api_router.include_router(router, prefix='/api')
