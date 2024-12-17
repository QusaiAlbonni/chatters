from asgiref.sync import sync_to_async
from langdetect import detect
from .models import Message

from lingua import Language, LanguageDetectorBuilder
languages = Language.all()
detector = LanguageDetectorBuilder.from_languages(*languages).build()


@sync_to_async
def detect_lang(text: str):
    return detector.detect_language_of(text).iso_code_639_1.name.lower()

async def detect_message_lang(message: Message):
    return await detect_lang(text=message.content)