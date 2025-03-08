import time
from datetime import datetime
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict

import logging
import os

now = datetime.now()
LOG_DIR = "/logs"
LOG_FILE = os.path.join(LOG_DIR, f"{now.strftime("%d_%m_%Y_%H_%M")}_server.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.info("Application started!")


class Settings(BaseSettings):
    postgres_password: str
    postgres_user: str
    postgres_db: str
    app_url: str

    filestorage: str = "/xml_doc_creator_nginx_docker/filestorage"

    @property
    def postgres_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{quote_plus(self.postgres_password)}@postgres/{self.postgres_db}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
