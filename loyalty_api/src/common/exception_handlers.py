from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from src.common.responses import ApiResponse
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        ApiResponse(errors=[exc.detail], result=None, success=False).dict(),
        status_code=exc.status_code,
        headers=getattr(exc, "headers", None),
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiResponse(
            errors=jsonable_encoder(exc.errors()), result=None, success=False
        ).dict(),
    )
