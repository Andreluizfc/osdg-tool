from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import traceback

from core.fos.fos_extractor import FosExtractor
from core.sdg.sdg_tagger import SdgTagger


main_router = APIRouter()

fos_extractor = FosExtractor()
sdg_tagger = SdgTagger()


class TagInput(BaseModel):
    text: str
    detailed: Optional[bool] = False


class TagManyInput(BaseModel):
    texts: List[str]
    detailed: Optional[bool] = False


with open('templates/index.html', 'r') as file_:
    index_html = file_.read()


@main_router.get('/')
async def home():
    return HTMLResponse(content=index_html)


@main_router.post('/tag')
async def tag(item: TagInput):
    try:
        fos = fos_extractor.extract(item.text)
        sdgs = sdg_tagger.tag(fos, detailed=item.detailed)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(ex), 'meta': traceback.format_exc(), 'status': 'ERROR'})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'result': sdgs, 'status': 'OK'})


@main_router.post('/tag_many')
async def tag_many(item: TagManyInput):
    try:
        foses = fos_extractor.extract_many(item.texts)
        sdgs = sdg_tagger.tag_many(foses, detailed=item.detailed)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': str(ex), 'meta': traceback.format_exc(), 'status': 'ERROR'})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'result': sdgs, 'status': 'OK'})