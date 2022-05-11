from typing import Any


def std_response(status: int, info: Any):
    return {
        "status": status,
        "info": info
    }
