import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.api import api_router
from src.core import config

app = FastAPI()

if config.settings.CORS_ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.settings.CORS_ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=['GET', 'POST', 'PATCH', 'DELETE', 'get', 'post', 'patch', 'delete'],
        allow_headers=['*'],
    )

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=4001, reload=True, access_log=False)
