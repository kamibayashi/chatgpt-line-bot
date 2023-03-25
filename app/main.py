import logging

import sentry_sdk
from aiolinebot import AioLineBotApi
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import OpenAIChat
from linebot import WebhookParser
from linebot.models import TextMessage
from sentry_sdk import capture_exception
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.database import get_db
from app.core.logger import get_logger

# init logger
logger = get_logger(__name__)

# init sentry

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

if settings.SENTRY_SDK_DNS:
    sentry_sdk.init(
        dsn=settings.SENTRY_SDK_DNS,
        environment=settings.ENV,
        integrations=[sentry_logging, SqlalchemyIntegration()],
        traces_sample_rate=1.0,
    )


# init fastapi
app = FastAPI(
    title=f"{settings.BASE_CONFIG.APP_NAME} [{settings.ENV}]",
    version=settings.BASE_CONFIG.APP_VERSION,
    debug=settings.BASE_CONFIG.DEBUG or False,
)

app.add_middleware(SentryAsgiMiddleware)

# init line bot
line_bot_api = AioLineBotApi(channel_access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
webhook_parser = WebhookParser(channel_secret=settings.LINE_CHANNEL_SECRET)

# init openai
llm = OpenAIChat(
    model_name=settings.MODEL_NAME,
    temperature=settings.TEMPUTURE,
    max_tokens=settings.MAX_TOKENS,
    prefix_messages=[{"role": "system", "content": settings.BASE_CHARACTOR}],
)

prompt = PromptTemplate(
    input_variables=["history", "input"], template=settings.TEMPLATE
)

conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=ConversationBufferWindowMemory(k=4, memory_key="history"),
    verbose=True,
)


async def event_handler(events, db) -> None:
    for ev in events:
        try:
            logger.log(logging.INFO, f"reply message: {ev.message.text}")
            event = crud.create_event_by_line(db=db, event=ev)
            reply = crud.create_reply_message_by_chatgpt(
                db=db, event=event, reply=query_openai(event.message_text)
            )
            await line_bot_api.reply_message_async(
                event.reply_token, TextMessage(text=reply.message_text)
            )
        except Exception as err:
            capture_exception(err)


def query_openai(message: str) -> str:
    return conversation.predict(input=message)


@app.post("/callback")
async def callback(
    request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
) -> str:
    events = webhook_parser.parse(
        (await request.body()).decode(settings.DECODE),
        request.headers.get("X-Line-Signature", ""),
    )
    background_tasks.add_task(event_handler, events=events, db=db)

    return "ok"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
