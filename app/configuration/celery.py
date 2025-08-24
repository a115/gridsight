from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_user: str
    redis_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def broker_url(self) -> str:
        return f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}"

    @property
    def result_backend(self) -> str:
        return f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}"


celery_settings = CelerySettings()
