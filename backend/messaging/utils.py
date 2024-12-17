from asgiref.sync import sync_to_async
from langdetect import detect
from .models import Message


@sync_to_async
def detect_lang(text: str):
    return detect(text)

async def detect_message_lang(message: Message):
    return await detect_lang(text=message.content)