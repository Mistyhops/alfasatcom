import datetime
import json

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import ResponseObject


class DBManager:

    def __init__(self, request, session):
        self.request = request
        self.session: AsyncSession = session

    async def get_obj(self) -> ResponseObject:
        query = text(self._get_obj_select_query())
        data = await self.session.execute(query)

        cols = data.keys()
        data = data.fetchone()

        if data:
            dict_data = dict(zip(cols, data))
            model_data = ResponseObject(
                id=dict_data.get('id'),
                name=dict_data.get('name'),
                value=json.dumps(dict_data.get('value')),
                date_update=dict_data.get('date_update'),
            )
            return model_data
        return None

    async def get_data(self) -> list[ResponseObject]:
        query = text(self._get_select_query())
        data = await self.session.execute(query)

        cols = data.keys()
        list_data = [dict(zip(cols, row)) for row in data.fetchall()]

        items = []

        for obj in list_data:
            item = ResponseObject(
                id=obj.get('id'),
                name=obj.get('name'),
                value=json.dumps(obj.get('value')),
                date_update=obj.get('date_update'),
            )

            items.append(item)

        return items

    async def post_data(self) -> ResponseObject:
        query = text(self._get_insert_query())
        data = await self.session.execute(query)
        await self.session.commit()

        cols = data.keys()
        dict_data = dict(zip(cols, data.fetchone()))

        model_data = ResponseObject(
            id=dict_data.get('id'),
            name=dict_data.get('name'),
            value=json.dumps(dict_data.get('value')),
            date_update=dict_data.get('date_update'),
        )

        return model_data

    async def patch_data(self, obj_id: int) -> ResponseObject:
        query = text(self._get_update_query(obj_id))
        data = await self.session.execute(query)
        await self.session.commit()

        cols = data.keys()
        data = data.fetchone()

        if data:
            dict_data = dict(zip(cols, data))
            model_data = ResponseObject(
                id=dict_data.get('id'),
                name=dict_data.get('name'),
                value=json.dumps(dict_data.get('value')),
                date_update=dict_data.get('date_update'),
            )

            return model_data
        return None

    async def delete_data(self) -> ResponseObject:
        query = text(self._get_delete_query())
        data = await self.session.execute(query)
        await self.session.commit()

        cols = data.keys()
        data = data.fetchone()

        if data:
            dict_data = dict(zip(cols, data))
            model_data = ResponseObject(
                id=dict_data.get('id'),
                name=dict_data.get('name'),
                value=json.dumps(dict_data.get('value')),
                date_update=dict_data.get('date_update'),
            )

            return model_data
        return None

    def _get_obj_select_query(self) -> str:
        obj_id = self.request.obj_id

        query = f"""
SELECT id, name, value, date_update
    FROM test
    WHERE id = {obj_id};
        """

        return query

    def _get_select_query(self) -> str:
        query = f"""
SELECT id, name, value, date_update
    FROM test
    ORDER BY id;
        """

        return query

    def _get_insert_query(self) -> str:
        name = self.request.name
        value = json.dumps(self.request.value)
        date_update = datetime.datetime.now()

        query = f"""
INSERT INTO test (name, value, date_update)
    VALUES
    ('{name}', '{value}', '{date_update}')
    RETURNING id, name, value, date_update;
        """

        return query

    def _get_update_query(self, obj_id: int) -> str:
        name = self.request.name
        value = json.dumps(self.request.value) if self.request.value else None
        date_update = datetime.datetime.now()

        query = f"""
UPDATE test
    SET {f"name = '{name}'," if name else ""}
        {f"value = '{value}'," if value else ""}
        date_update = '{date_update}'
    WHERE id = {obj_id}
    RETURNING id, name, value, date_update;
        """

        return query

    def _get_delete_query(self) -> str:
        obj_id = self.request.obj_id

        query = f"""
DELETE FROM test WHERE id = {obj_id}
    RETURNING id, name, value, date_update;
        """

        return query
