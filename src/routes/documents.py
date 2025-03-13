import os

from fastapi import APIRouter, Depends, HTTPException, Request
from config import settings
from helpers.db import get_async_session
from pydantic import ValidationError
from starlette.responses import RedirectResponse, FileResponse
from starlette.status import HTTP_303_SEE_OTHER

from . import templates
from models import DocumentModel
from schemas import DocumentCreateSchema
from schemas import EntityIdType, TradingCapacityType, BuySellIndicatorType

from config import logger

documents_router = APIRouter()


@documents_router.get("/create-form")
async def create_form(request: Request):
    try:
        return templates.TemplateResponse("create_form.html", {
            "request": request,
            "EntityIdType": EntityIdType,
            "TradingCapacityType": TradingCapacityType,
            "BuySellIndicatorType": BuySellIndicatorType
        })
    except Exception as e:
        return templates.TemplateResponse("create_form.html", {"request": request, "error_message": f"An unexpected error occurred. {e}"})

@documents_router.get("/update-form/{document_id}")
async def update_document(
        request: Request,
        document_id: int = None,
        db = Depends(get_async_session)
):

    existing_document = await db.get(DocumentModel, document_id)

    if not existing_document:
        raise HTTPException(status_code=404, detail="Document not found")

    existing_document_data = {
        "reportingEntityId": existing_document.reportingEntityId,
        "reportingEntityIdType": existing_document.reportingEntityIdType,
        "recordSeqNumber": existing_document.recordSeqNumber,
        "idOfMarketParticipant": existing_document.idOfMarketParticipant,
        "idOfMarketParticipantType": existing_document.idOfMarketParticipantType,
        "otherMarketParticipant": existing_document.otherMarketParticipant,
        "otherMarketParticipantType": existing_document.otherMarketParticipantType,
        "tradingCapacity": existing_document.tradingCapacity,
        "buySellIndicator": existing_document.buySellIndicator,
        "contractId": existing_document.contractId,
        "document_id": document_id,
    }


    return templates.TemplateResponse("update_form.html", {
        "request": request,
        "EntityIdType": EntityIdType,
        "TradingCapacityType": TradingCapacityType,
        "BuySellIndicatorType": BuySellIndicatorType,
        "document": existing_document_data
    })


@documents_router.get("/list")
async def docs_list(
        request: Request,
        page: int = 1,
        limit: int = 10,
        db = Depends(get_async_session)
):
    documents = await DocumentModel.get_list(db, page, limit)
    return templates.TemplateResponse("documents_list.html", {"request": request, "documents": documents})

@documents_router.post("/create")
async def new_doc(
        request: Request,
        db = Depends(get_async_session),
):
    form = await request.form()

    try:
        document_data = DocumentCreateSchema(**form)
        await DocumentModel.create(db, document_data)
        return RedirectResponse(url="/documents/list", status_code=HTTP_303_SEE_OTHER)

    except ValidationError as e:
        error_messages = [f"{error['msg']}" for error in e.errors()]
        return templates.TemplateResponse("create_form.html", {
            "request": request,
            "error_message": " :: ".join(error_messages),
        })
    except ValueError as e:
        error_message = str(e)
        return templates.TemplateResponse("create_form.html", {"request": request, "error_message": error_message})
    except Exception as e:
        return templates.TemplateResponse("create_form.html", {
            "request": request,
            "error_message": f"An unexpected error occurred. {e}"
        })


@documents_router.get("/archive/{document_id}")
async def archive_doc(
        request: Request,
        document_id: int,
        db = Depends(get_async_session)
):
    await DocumentModel.delete(db, document_id)
    return RedirectResponse(url="/documents/list", status_code=HTTP_303_SEE_OTHER)

@documents_router.get("/download/{file_name}")
async def download_file(file_name: str):
    full_path = os.path.join(settings.filestorage, file_name)

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path, media_type="application/octet-stream", filename=file_name)
