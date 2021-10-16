from dotenv import load_dotenv
from os import path, getenv


def check_env():
    if path.exists("local.env"):
        return load_dotenv("local.env")
    load_dotenv()


check_env()


class Config:
    API_ID = int(getenv("API_ID"))
    API_HASH = getenv("API_HASH")
    BOT_TOKEN = getenv("BOT_TOKEN")
    SESSION = getenv("SESSION")


config = Config()
