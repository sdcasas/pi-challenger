import logging

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from starlette.responses import JSONResponse

from apps.router import router as router_character
from settings.config_logging import LoggingMiddleware, EndpointFilter
from settings.config import (
        APP_NAME,
        APP_VERSION,
        APP_DESCRIPTION,
        DOCS_URL,
)


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url=DOCS_URL,
    redoc_url=None,
    swagger_ui_parameters={"docExpansion": "none"},
)

# URLs
app.include_router(router_character, tags=['Character'], prefix='/character')

# logging
app.add_middleware(LoggingMiddleware)
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

# service check available
@app.get("/ping")
def ping():
    return {"ping": "pong!"}


# error manager
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    fields = []
    for error in exc.errors():
        fields.append(error.get("loc")[-1])
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {
                "detail": f"Verifique los valores ingresados para: {fields}"
            }
        ),
    )
