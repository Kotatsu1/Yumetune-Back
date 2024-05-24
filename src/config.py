from dotenv import dotenv_values

class Config():
    MODE: str
    ENV_VALUES: dict

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    CORS_ORIGINS: list
    CORS_METHODS: list
    CORS_HEADERS: list

    REFRESH_TOKEN_EXPIRE_DAYS: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    def set_mode(self, mode):
        self.MODE = mode

    
    def update_config(self):
        dotenv_path = f".env.{self.MODE}"
        self.ENV_VALUES = dotenv_values(dotenv_path)
        
        for key, value in self.ENV_VALUES.items():
            setattr(self, key, value)


    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


config = Config()
