from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    APP_NAME: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int

    JWT_SECRET: str
    JWT_ALGO: str
    JWT_EXPIRE_HOURS: int

    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()
