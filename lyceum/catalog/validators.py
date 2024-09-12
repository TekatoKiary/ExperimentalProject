import re

from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

__all__ = []


@deconstructible
class ValidateMustContain(BaseValidator):
    regex = r"\b({})\b"

    def __init__(self, *word_to_check, message=None, code=None):
        super().__init__(message, code)
        self.words_to_check = word_to_check
        self.regex = self.regex.format("|".join(self.words_to_check))

    def __call__(self, value):
        if not re.search(self.regex, value.lower()):
            raise ValidationError(
                f"В тексте не написано хотя бы одно слово такие как: "
                f"{', '.join(self.words_to_check)}.",
            )

    def __eq__(self, other):
        super().__eq__(other)
