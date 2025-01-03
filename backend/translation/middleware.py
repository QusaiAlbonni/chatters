from typing import Any
from django.http import HttpRequest
from .services import LanguageService
from .services import Langauge
from django.utils.translation.trans_real import parse_accept_lang_header

class LanguageMiddleware:
    def __init__(self, get_response, language_service: LanguageService = LanguageService()) -> None:
        self.get_response = get_response
        self.language_service = language_service
    def __call__(self, request: HttpRequest) -> Any:
        raw_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        accept_lang = parse_accept_lang_header(raw_language)
        if accept_lang:
            accept_lang, unused = accept_lang[0]
        else:
            accept_lang = 'en'
        try:
            language_code = self.language_service.sync_get_language(accept_lang.split('-')[0]).code
        except Langauge.DoesNotExist as e:
            if raw_language != '':
                print(accept_lang)
                raise e
            language_code = 'en'
        
        setattr(request, 'language', language_code)
        
        response = self.get_response(request)
        return response