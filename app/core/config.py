import os

from pydantic import BaseSettings

from app.core import BaseConfig, get_base_config


class Settings(BaseSettings):
    ENV: str = os.getenv("BUILD_ENV", "")
    BASE_CONFIG: BaseConfig = get_base_config()
    SENTRY_SDK_DNS: str = os.getenv("SENTRY_SDK_DNS", "")

    LINE_CHANNEL_ACCESS_TOKEN: str = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    LINE_CHANNEL_SECRET: str = os.environ["LINE_CHANNEL_SECRET"]
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

    DECODE: str = "utf-8"

    MODEL_NAME: str = "gpt-3.5-turbo"
    TEMPUTURE: float = 0.7
    MAX_TOKENS: int = 1000

    TEMPLATE: str = """あなたは全知全能の全てを知っているAIでHumanと会話しています。

{history}
Human: {input}
AI:"""
    BASE_CHARACTOR: str = """あなたは、親切で、創造的で、賢く、とてもフレンドリーで役に立つ女性のAI assistantです。"""


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
