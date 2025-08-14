from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    bmrs_api_key: str

    model_config = SettingsConfigDict(extra="ignore")

app_settings = AppSettings()
