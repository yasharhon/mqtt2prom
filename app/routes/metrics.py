from typing import Any

from fastapi import APIRouter, Request, Response

metrics_router = APIRouter(prefix="/metrics")


@metrics_router.get("/")
def get_data(request: Request) -> Response:
    state: dict[str, Any] = request.app.state.latest

    ret = "\n".join(f"{key}={val}" for key, val in state.items())

    return Response(content=ret, media_type="text/plain")
