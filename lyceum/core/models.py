from django.core import exceptions, validators
from django.db import models

from core.utils import normalize_data

__all__ = []


class NameAndPublishAbstractModel(models.Model):
    name = models.CharField(
        verbose_name="название",
        unique=True,
        max_length=150,
        help_text="Напишите имя",
    )
    is_published = models.BooleanField(
        verbose_name="опубликовано",
        default=True,
    )

    class Meta:
        abstract = True


class SlugAndNormalizeNameAbstractModel(models.Model):
    slug = models.SlugField(
        "Слаг",
        unique=True,
        validators=[
            validators.MaxLengthValidator(200),
        ],
        help_text="Напишите слаг",
    )

    normalize_name = models.CharField(
        editable=False,
        blank=True,
        max_length=150,
    )

    class Meta:
        abstract = True

    def clean(self):
        self.create_normalise_data()
        super().clean()

    def create_normalise_data(self):
        value = normalize_data(self.name)
        if value not in [
            i.normalize_name
            for i in self.__class__.objects.all()
            if self.name != i.name
        ]:
            self.normalize_name = value
        else:
            raise exceptions.ValidationError("Данное имя уже существует")
