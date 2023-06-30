from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Type, Union
import fastapi
from fastapi.datastructures import Default
from fastapi.params import Depends
from fastapi.routing import APIRoute, BaseRoute
from fastapi.testclient import TestClient
from fastapi.utils import generate_unique_id
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Lifespan

import fastdry.cr


class Router(fastdry.cr.ClassRouter):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    @property
    def some_random_property(self):
        """test to make sure this is not accessed during initialization of the router"""
        raise AttributeError("Should not be accessed")

    @fastdry.cr.get("/hello")
    def get(self) -> dict:
        return {"hello": self.name}

    @fastdry.cr.get("/hallo")
    def get_hallo(self) -> dict:
        return {"hallo": self.name}

    @fastdry.cr.post("/hello")
    def post(self) -> dict:
        return {"post": self.name}


def test_get_decorator():
    @fastdry.cr.get("/test")
    def test():
        return {"message": "Hello World"}

    assert hasattr(test, "_fastdry_cr")
    data = test._fastdry_cr
    assert data["methods"] == ["GET"]


def test_class_router():
    app = fastapi.FastAPI()
    app.include_router(Router("world"), prefix="/world")
    app.include_router(Router("test"), prefix="/test")

    client = TestClient(app)
    response = client.get("/world/hello")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}

    response = client.get("/world/hallo")
    assert response.status_code == 200
    assert response.json() == {"hallo": "world"}

    response = client.post("/world/hello")
    assert response.status_code == 200
    assert response.json() == {"post": "world"}

    response = client.get("/test/hello")
    assert response.status_code == 200
    assert response.json() == {"hello": "test"}
