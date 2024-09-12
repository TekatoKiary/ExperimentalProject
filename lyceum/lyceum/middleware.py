import re

import django.conf

__all__ = []


class ReverseRussianWordsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.call_count = 0

    def __call__(self, request):
        response = self.get_response(request)
        if django.conf.settings.ALLOW_REVERSE:
            self.call_count = (self.call_count + 1) % 10
            if self.call_count == 0:
                response.content = self.reverse_russian_words_in_content(
                    response.content.decode(),
                ).encode()
        return response

    def reverse_russian_words_in_content(self, content: str):
        def reverse(match):
            return match.group()[::-1]

        return re.sub(r"\b[а-яА-ЯёЁ]+\b", reverse, content)
