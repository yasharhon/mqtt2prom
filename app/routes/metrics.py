from typing import Any

from fastapi import APIRouter, Request, Response

metrics_router = APIRouter(prefix="/metrics")

TOPIC_FILTER_LABEL = "source"


@metrics_router.get("")
def get_data(request: Request) -> Response:
    state_for_topics: dict[str, dict[str, Any]] = request.app.state.polled_data

    ret = "\n".join(
        "\n".join(
            f'{key}{{{TOPIC_FILTER_LABEL}="{topic_name}"}} {val}'
            for key, val in data.items()
            if type(val) in [int, float]  # This should be unit tested
        )
        for topic_name, data in state_for_topics.items()
    )

    return Response(content=ret, media_type="text/plain")
