from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_FILE: str = "data/database.csv"
    PDF_SERVICE_KEY: str
    FILE_NAME_TO_PATH: dict[str, str] = {
        "healthinc.pdf": "assets/healthinc.pdf",
        "retailco.pdf": "assets/retailco.pdf",
        "financellc.pdf": "assets/financellc.pdf",
        "techcorp.pdf": "assets/techcorp.pdf",
    }

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
