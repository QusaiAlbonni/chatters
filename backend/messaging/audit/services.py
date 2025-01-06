from .models import PromptLog, Message, Langauge

class LogPromptsService:
    async def alog(self, message: Message, prompt: str, response: str, to_language: Langauge) -> PromptLog:
        return (await PromptLog.objects.acreate(message = message, prompt= prompt, to_language= to_language, reply=response))