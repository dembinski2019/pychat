from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .route.api import api
from .w_sockets.api import ws_api
from .w_sockets.ws_chat import chat

app = FastAPI()


app.include_router(api)
app.include_router(ws_api)


app.mount("/static", StaticFiles(directory="static"), name="static")
