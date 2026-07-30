from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(tags=["Pages"])

# __file__ = app/routers/pages.py → dirname = app/routers → parent = app/
_templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

templates = Jinja2Templates(directory=_templates_dir)


@router.get("/", include_in_schema=False)
async def dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})


@router.get("/new-meeting", include_in_schema=False)
async def new_meeting_page(request: Request):
    return templates.TemplateResponse(request=request, name="new-meeting.html", context={"request": request})


@router.get("/meetings/{meeting_id}", include_in_schema=False)
async def meeting_detail_page(request: Request, meeting_id: int):
    return templates.TemplateResponse(request=request, name="meeting-detail.html", context={"request": request})


@router.get("/history", include_in_schema=False)
async def history_page(request: Request):
    return templates.TemplateResponse(request=request, name="history.html", context={"request": request})
