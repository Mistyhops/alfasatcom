from fastapi import APIRouter, Depends
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api import deps
from src.db_manager import DBManager
from src.schemas import RequestPost, ResponseObject, RequestPatch, RequestDelete, RequestGet

router = APIRouter()


@router.get(
    path='/',
    response_model=list[ResponseObject],
    status_code=200
)
async def get_all(
        session: AsyncSession = Depends(deps.get_session)
):
    try:
        request = {}
        db_manager = DBManager(
            request=request,
            session=session,
        )
        result = await db_manager.get_data()
        return result
    except ValidationError as e:
        exception_messages = [exc['msg'] for exc in e.errors()]
        return JSONResponse(
            status_code=422, content=exception_messages
        )
    except Exception as e:
        return JSONResponse(
            status_code=400, content=e
        )


@router.get(
    path='/{obj_id}/',
    response_model=ResponseObject,
    status_code=200
)
async def get_one(
        obj_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    try:
        request = RequestGet(obj_id=obj_id)
        db_manager = DBManager(
            request=request,
            session=session,
        )
        result = await db_manager.get_obj()
        if not result:
            return JSONResponse(status_code=404, content='object not found')
        return result
    except ValidationError as e:
        exception_messages = [exc['msg'] for exc in e.errors()]
        return JSONResponse(
            status_code=422, content=exception_messages
        )
    except Exception as e:
        return JSONResponse(
            status_code=400, content=e
        )


@router.post(
    path='/',
    response_model=ResponseObject,
    status_code=201
)
async def post(
        request: RequestPost,
        session: AsyncSession = Depends(deps.get_session)
):
    try:
        db_manager = DBManager(
            request=request,
            session=session,
        )
        result = await db_manager.post_data()
        return result.dict()
    except ValidationError as e:
        exception_messages = [exc['msg'] for exc in e.errors()]
        return JSONResponse(
            status_code=422, content=exception_messages
        )
    except Exception as e:
        return JSONResponse(
            status_code=400, content=e
        )


@router.patch(
    path='/{obj_id}/',
    response_model=ResponseObject,
    status_code=201
)
async def patch(
        obj_id: int,
        request: RequestPatch,
        session: AsyncSession = Depends(deps.get_session)
):
    try:
        if any(request.dict().values()):
            db_manager = DBManager(
                request=request,
                session=session,
            )
            result = await db_manager.patch_data(obj_id)
            if not result:
                return JSONResponse(status_code=404, content='object not found')
            return result.dict()
        else:
            error_text = 'No data to update'
            return JSONResponse(
                status_code=422, content=error_text
            )
    except ValidationError as e:
        exception_messages = [exc['msg'] for exc in e.errors()]
        return JSONResponse(
            status_code=422, content=exception_messages
        )
    except Exception as e:
        return JSONResponse(
            status_code=400, content=e
        )


@router.delete(
    path='/{obj_id}/',
    response_model=ResponseObject,
    status_code=200
)
async def delete(
        obj_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    try:
        request = RequestDelete(obj_id=obj_id)
        db_manager = DBManager(
            request=request,
            session=session,
        )
        result = await db_manager.delete_data()
        if not result:
            return JSONResponse(status_code=404, content='object not found')
        return result
    except ValidationError as e:
        exception_messages = [exc['msg'] for exc in e.errors()]
        return JSONResponse(
            status_code=422, content=exception_messages
        )
    except Exception as e:
        return JSONResponse(
            status_code=400, content=e
        )
