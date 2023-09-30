import fastapi
from fastapi.testclient import TestClient

import fastdry.cr


class Router(fastdry.cr.ClassRouter):
    def __init__(self, name) -> None:
        self.name = name
        super().__init__()

    @property
    def some_random_property(self):
        """test to make sure this is not accessed during initialization of the router"""
        raise AttributeError("Should not be accessed")  # pragma: nocover

    @fastdry.cr.head("/hello")
    def head(self) -> dict:
        return {}

    @fastdry.cr.get("/hello", summary="Say hello to {self.name}", description="More about {self.name}", operation_id="custom_hello_{self.name}", name="Hello {self.name}", tags=["foo", "bar", "{self.name}", "{self.name}!"])
    def get(self) -> dict:
        return {"hello": self.name}

    @fastdry.cr.get("/hi/{more}")
    def get_hi(self, more: int) -> dict:
        return {"hi": self.name, "more": 1}

    @fastdry.cr.post("/hello")
    def post(self) -> dict:
        return {"post": self.name}

    @fastdry.cr.put("/hello")
    def put(self) -> dict:
        return {"put": self.name}
    
    @fastdry.cr.delete("/hello")
    def delete(self) -> dict:
        return {"delete": self.name}

    @fastdry.cr.patch("/hello")
    def patch(self) -> dict:
        return {"patch": self.name}

    @fastdry.cr.options("/hello")
    def options(self) -> dict:
        return {"options": self.name}
    
    @fastdry.cr.trace("/hello")
    def trace(self) -> dict:
        return {"trace": self.name}
    

def test_get_decorator():
    @fastdry.cr.get("/test")
    def test():
        return {"message": "Hello World"} # pragma: nocover

    assert hasattr(test, "_fastdry_cr")
    data = test._fastdry_cr
    assert data["methods"] == ["GET"]


def test_class_router():
    app = fastapi.FastAPI()
    app.include_router(Router("world"), prefix="/world")
    app.include_router(Router("test"), prefix="/test")

    client = TestClient(app)

    for path in ("world", "test"):
        # head request
        response = client.head(f"/{path}/hello")
        assert response.status_code == 200
        assert response.text == ""

        # get request
        response = client.get(f"/{path}/hello")
        assert response.status_code == 200
        assert response.json() == {"hello": path}

        # get request, different path and a path argument
        response = client.get(f"/{path}/hi/1")
        assert response.status_code == 200
        assert response.json() == {"hi": path, "more": 1}

        # post request
        response = client.post(f"/{path}/hello")
        assert response.status_code == 200
        assert response.json() == {"post": path}

        # put request
        response = client.put(f"/{path}/hello")
        assert response.status_code == 200
        assert response.json() == {"put": path}

        # delete request
        response = client.delete(f"/{path}/hello")
        assert response.status_code == 200
        assert response.json() == {"delete": path}

        # patch request
        response = client.patch(f"/{path}/hello")
        assert response.status_code == 200
        assert response.json() == {"patch": path}

        # options request
        response = client.options(f"/{path}/hello")
        assert response.status_code == 200
        assert response.json() == {"options": path}

        # trace request
        response = client.request("TRACE", f"/{path}/hello")
        assert response.status_code == 200
        assert response.json() == {"trace": path}


def test_summary_formatting():
    app = fastapi.FastAPI()
    app.include_router(Router("world"), prefix="/world")
    app.include_router(Router("test"), prefix="/test")

    client = TestClient(app)

    schema_request = client.get("/openapi.json")
    schema = schema_request.json()

    for path in ("world", "test"):
        hello_get = schema["paths"][f"/{path}/hello"]["get"]

        assert hello_get["summary"] == f"Say hello to {path}"
        assert hello_get["description"] == f"More about {path}"
        assert hello_get["operationId"] == f"custom_hello_{path}"
        assert hello_get["tags"] == ["foo", "bar", path, f"{path}!"]
        