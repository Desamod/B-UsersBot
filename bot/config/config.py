from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    SLEEP_TIME: list[int] = [7200, 10800]
    START_DELAY: list[int] = [25, 55]
    AUTO_TASK: bool = True
    JOIN_TG_CHANNELS: bool = True
    USE_PROXY_FROM_FILE: bool = False
    REF_ID: str = 'ref-r2RLzW1YK4Q4SjJk7vHHEU'
    DISABLED_TASKS: list[str] = ['CONNECT_WALLET', 'INVITE_FRIENDS', 'BOOST_TG']


settings = Settings()
