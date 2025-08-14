from pydantic_settings import BaseSettings, SettingsConfigDict


class DjangoSettings(BaseSettings):
    secret_key: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="DJANGO_",
        extra="ignore",
    )

django_settings = DjangoSettings()
