from abc import ABC, abstractmethod
from messaging.models import Langauge

class LanguageServiceBase(ABC):
    @abstractmethod
    async def get_language(self, code: str) -> Langauge:
        ...
    def sync_get_language(self, code: str) -> Langauge:
        ...

class LanguageService(LanguageServiceBase):
    
    async def get_language(self, code: str) -> Langauge:
        return await Langauge.objects.filter(code__icontains = code).afirst()
    
    def sync_get_language(self, code: str) -> Langauge:
        return Langauge.objects.filter(code__icontains = code).first()