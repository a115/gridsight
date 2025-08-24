from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str
    bmrs_api_key: str
    logfire_token: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_settings = AppSettings()
