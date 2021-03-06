import os


SECRET_KEY = os.environ.get("SECRET_KEY")
ACCESS_TOKEN_LIFETIME = 1200  # 20 minutes for access token
REFRESH_TOKEN_LIFETIME = 432000  # 5 days for refresh token
