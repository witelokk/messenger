from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    redis_host: str
    redis_port: str
    bot_token: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
