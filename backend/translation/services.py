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
        language= await Langauge.objects.filter(code__icontains = code).afirst()
        
        if not language:
            raise Langauge.DoesNotExist()
        
        return language
    
    def sync_get_language(self, code: str) -> Langauge:
        langauge = Langauge.objects.filter(code__icontains = code).first()
        
        if not langauge :
            raise Langauge.DoesNotExist()
        
        return langauge
    