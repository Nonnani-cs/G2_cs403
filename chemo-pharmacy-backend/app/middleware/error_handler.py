from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.utils.constants import SQLITE_LOCK_ERROR


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_error_handler(_: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "error_code": "HTTP_ERROR",
                "message": str(exc.detail),
                "details": {},
            },
        )

    @app.exception_handler(OperationalError)
    async def sqlite_error_handler(_: Request, exc: OperationalError):
        message = str(exc.orig) if getattr(exc, "orig", None) else str(exc)
        status_code = 503 if "locked" in message.lower() else 500
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "error",
                "error_code": SQLITE_LOCK_ERROR if status_code == 503 else "DB_ERROR",
                "message": message,
                "details": {},
            },
        )
