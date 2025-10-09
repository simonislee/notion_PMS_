import dotenv
from pydantic.v1 import BaseSettings


class EnvSettings(BaseSettings):
    NOTION_API: str


def get_notion_api():
    dotenv.load_dotenv()
    setting = EnvSettings()
    return setting.NOTION_API
