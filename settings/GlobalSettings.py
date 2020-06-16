from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_STRING: str = ''
    JWT_KEY: str = 'sampleKey'


settings = Settings()
