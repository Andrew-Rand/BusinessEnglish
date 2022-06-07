import datetime
from typing import Callable, Any

import jwt

from src.user.constants import SECRET_KEY


def create_token(user_id: str, time_delta_seconds: int) -> str:

    token_payload = {
        'id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=time_delta_seconds),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
    return token


def login_required(func: Any) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Response:
        token = request.headers['token']
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'http://localhost:8000/refresh'})
        except jwt.InvalidTokenError:
            return jsonify({'Message': 'Invalid token. Please log in again.'})
        return func(*args, **kwargs)

    return wrapper
