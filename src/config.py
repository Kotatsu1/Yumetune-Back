import os

class Config():
    def __init__(self):
        self.update_config()

    DATABASE_URL: str

    CORS_ORIGINS=["http://localhost:5173"]
    CORS_METHODS=["*"]
    CORS_HEADERS=["*"]

    REFRESH_TOKEN_EXPIRE_DAYS=30
    ACCESS_TOKEN_EXPIRE_MINUTES=60

    SECRET_KEY: str

    
    def update_config(self):
        for key, value in os.environ.items():
            if key in os.environ:
                setattr(self, key, value)

config = Config()

