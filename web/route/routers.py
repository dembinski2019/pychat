from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

template = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, summary="Chat")
async def get(request:Request):
    return template.TemplateResponse('chat.html', {"request": request})