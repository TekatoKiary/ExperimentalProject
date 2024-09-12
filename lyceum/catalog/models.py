from ckeditor.fields import RichTextField
from django.core import validators
from django.db import models
from django.utils.html import mark_safe
from sorl.thumbnail import get_thumbnail

from catalog.validators import ValidateMustContain
from core.models import (
    NameAndPublishAbstractModel,
    SlugAndNormalizeNameAbstractModel,
)

__all__ = []


class Category(NameAndPublishAbstractModel, SlugAndNormalizeNameAbstractModel):
    weight = models.IntegerField(
        "Вес",
        default=100,
        validators=[
            validators.MaxValueValidator(32767),
            validators.MinValueValidator(1),
        ],
        help_text="Напишите вес категории",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Tag(NameAndPublishAbstractModel, SlugAndNormalizeNameAbstractModel):
    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class ItemManager(models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related(
                Item.category.field.name,
                Item.main_image.field.name,
            )
            .prefetch_related(
                models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
            .only(
                Item.id.field.name,
                Item.name.field.name,
                Item.text.field.name,
                Item.main_image.field.name,
                "category__name",
            )
            .order_by("category__name", Item.name.field.name)
        )

    def on_main(self):
        return (
            self.get_queryset()
            .filter(
                is_published=True,
                is_on_main=True,
                category__is_published=True,
            )
            .select_related(
                Item.category.field.name,
                Item.main_image.field.name,
            )
            .prefetch_related(
                models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
            .only(
                Item.name.field.name,
                Item.text.field.name,
                Item.main_image.field.name,
                "category__name",
            )
            .order_by(Item.name.field.name)
        )


class Item(NameAndPublishAbstractModel):
    objects = ItemManager()

    text = RichTextField(
        "Текст",
        help_text="Опишите товар",
        validators=[ValidateMustContain("превосходно", "роскошно")],
    )

    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(
        "category",
        on_delete=models.CASCADE,
        related_query_name="category",
    )

    main_image = models.OneToOneField(
        "mainimage",
        on_delete=models.CASCADE,
        related_name="main_image",
        null=True,
        blank=True,
    )

    is_on_main = models.BooleanField(
        verbose_name="Опубликованный на главной странице",
        default=True,
    )

    created_time = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        auto_created=True,
        null=True,
        blank=True,
    )

    updated_time = models.DateTimeField(
        "Дата изменения",
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ("name", "category__name")

    def __str__(self):
        return self.name


class MainImage(models.Model):
    image = models.ImageField("Изображение", upload_to="catalog/main_images/")

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", quality=51)

    def get_image_50x50(self):
        return get_thumbnail(self.image, "50x50", quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50">')
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "Главное изображение"
        verbose_name_plural = "Главные изображения"

    def __str__(self):
        return str(self.image.url)


class Image(models.Model):
    image = models.ImageField(
        "Изображение",
        upload_to="catalog/images/%Y/%m/%d/",
    )
    item = models.ForeignKey(
        "item",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def get_image_50x50(self):
        return get_thumbnail(self.image, "50x50", quality=51)

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", quality=51)

    def image_tmb(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50">')
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return self.image.url
