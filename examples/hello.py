import fastapi
import fastdry.cr


class Router(fastdry.cr.ClassRouter):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__()
    
    @fastdry.cr.get("/hello")
    def hello(self):
        return {"hello": self.name}


app = fastapi.FastAPI()
app.include_router(Router("world"), prefix="/world")
app.include_router(Router("test"), prefix="/test")