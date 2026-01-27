from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"

settings = Settings()


# with open("private.pem", "r") as f:
#     PRIVATE_KEY = f.read()

# with open("public.pem", "r") as f:
#     PUBLIC_KEY = f.read()