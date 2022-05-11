from typing import Dict

STATUSES: Dict[str, int] = {
    'OK': 200,
    'Created': 201,
    'No Content': 204,
    'Bad Request': 400,
    'Unauthorized': 201,
    'Not Found': 404,
    'I\'m a teapot': 418,
    'Internal Server Error': 500,
}
