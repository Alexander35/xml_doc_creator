import logging

import uvicorn
from fastapi import FastAPI
from fastapi import Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from routes.documents import documents_router

server = FastAPI(root_path="/", docs_url="/docs",)

logger = logging.getLogger("server")



origins = [
    "http://localhost:8000",
    "http://localhost",
    "http://localhost:8080",
]
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#   Set directory public for urls
# server_api.mount("/filestorage", StaticFiles(directory="/express_accounting_docker/filestorage"), name="filestorage")


@server.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Database error occurred", "detail": str(exc)})


@server.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@server.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    error_text = "Parsing error"
    errors = exc.errors()
    if errors[0]:
        error_text = errors[0]['msg']

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "message": error_text,
                "detail": exc.errors(),
                "body": exc.body,
            }
        ),
    )

@server.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.png')

server.include_router(documents_router, prefix="/documents", tags=["documents"])


if __name__ == "__main__":
    uvicorn.run("main:server",
                host="127.0.0.1",
                port=3000,
                log_level="debug",
                reload=True)
