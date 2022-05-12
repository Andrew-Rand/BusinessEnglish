from typing import Any

from src.constants import STATUSES


def std_response(status: str, info: Any):
    return {
        "status": STATUSES.get(status),
        "info": info
    }
