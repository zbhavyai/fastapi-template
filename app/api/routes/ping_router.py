import logging

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/ping", response_class=PlainTextResponse, status_code=200)
async def ping() -> PlainTextResponse:
    logger.debug("ping")
    return PlainTextResponse("pong\n")
