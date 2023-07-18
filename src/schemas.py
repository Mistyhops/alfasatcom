from datetime import datetime
from typing import Union, Optional

from pydantic import BaseModel, Json, validator


class RequestGet(BaseModel):
    obj_id: int

    @classmethod
    @validator('obj_id')
    def is_id_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError('id must be positive number')
        return v


class RequestPost(BaseModel):
    name: str
    value: Json


class RequestPatch(BaseModel):
    name: Optional[str]
    value: Optional[Json]


class RequestDelete(BaseModel):
    obj_id: int

    @classmethod
    @validator('obj_id')
    def is_id_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError('id must be positive number')
        return v


class ResponseObject(BaseModel):
    id: int
    name: str
    value: Union[Json, dict]
    date_update: datetime
