import dotenv
from pydantic.v1 import BaseSettings


class EnvSettings(BaseSettings):
    NOTION_API_KEY: str
    LEASE_DATABASE: str
    PAYMENT_DATABASE: str


def get_notion_api():
    dotenv.load_dotenv()
    setting = EnvSettings()
    return setting.NOTION_API_KEY


def get_database_lease():
    dotenv.load_dotenv()
    setting = EnvSettings()
    return setting.LEASE_DATABASE


def get_database_payment():
    dotenv.load_dotenv()
    setting = EnvSettings()
    return setting.PAYMENT_DATABASE
