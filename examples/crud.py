from typing import TypeVar, Generic

import fastapi_offline
from fastdry import cr

import pydantic


ITEM_T = TypeVar("ITEM_T", bound=pydantic.BaseModel)


class ResponseLinks(pydantic.BaseModel):
    self: pydantic.HttpUrl
    next: pydantic.HttpUrl | None
    previous: pydantic.HttpUrl | None


class ListResponse(pydantic.BaseModel, Generic[ITEM_T]):
    links: ResponseLinks
    data: list[ITEM_T]


class GetResponse(pydantic.BaseModel, Generic[ITEM_T]):
    data: ITEM_T


STATE_CLS_T = TypeVar("STATE_CLS_T", bound=pydantic.BaseModel)


class CRUD2(cr.ClassRouter, Generic[STATE_CLS_T]):
    def __init__(self, collection_name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.collection_name = collection_name

    def _base_query(self) -> dict:
        # add query here, for example for auth
        return {}

    @cr.get("/")
    def list(self) -> GetResponse[STATE_CLS_T]:
        self._base_query()
        # data = db[self.collection_name].find(query)
        return {"data": [self.collection_name]}


def CRUD(state_cls: type, state_cls_out: type|None):

    if state_cls_out is None:
        state_cls_out = state_cls

    class CRUD(cr.ClassRouter):
        def __init__(self, collection_name: str, **kwargs) -> None:
            self.collection_name = collection_name
            super().__init__(**kwargs)

        def _base_query(self) -> dict:
            # add query here, for example for auth
            return {}

        @cr.get("/{resource_id}", summary="Get one entry from {self.collection_name}", name="Foo Bar")
        def get(self) -> GetResponse[state_cls_out]:
            self._base_query()
            # data = db[self.collection_name].find(query)
            return {"data": [self.collection_name]}

        @cr.get("/", summary="List {self.collection_name}")
        def list(self) -> ListResponse[state_cls]:
            self._base_query()
            # data = db[self.collection_name].find(query)
            return {"data": [self.collection_name]}

        @cr.post("/", summary="Create new entry in {self.collection_name}")
        def create(self, item: state_cls):
            self._base_query()
            # data = db[self.collection_name].find(query)
            return {"status": True}

        @cr.delete("/{resource_id}")
        def delete(self):
            return {"ok": True}

    return CRUD

