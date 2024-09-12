from django.contrib import admin
from django.utils.html import mark_safe

import catalog.models

__all__ = []


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.main_image:
            return mark_safe(
                f'<img src="/media/{obj.main_image.get_image_50x50()}">',
            )
        return "Изображение отсутствует"

    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
        "image_tag",
    )
    list_editable = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )

    list_display_links = (catalog.models.Item.name.field.name,)

    filter_horizontal = (catalog.models.Item.tags.field.name,)
    inlines = []

    readonly_fields = (
        catalog.models.Item.created_time.field.name,
        catalog.models.Item.updated_time.field.name,
    )


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (catalog.models.Tag.is_published.field.name,)

    list_display_links = (catalog.models.Tag.name.field.name,)

    fields = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
        catalog.models.Tag.slug.field.name,
    )


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
    )
    list_editable = (catalog.models.Category.is_published.field.name,)

    list_display_links = (catalog.models.Category.name.field.name,)

    fields = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
        catalog.models.Category.slug.field.name,
    )


@admin.register(catalog.models.MainImage)
class MainImageInline(admin.ModelAdmin):
    list_display = (catalog.models.MainImage.image_tmb,)


@admin.register(catalog.models.Image)
class ImageInline(admin.ModelAdmin):
    list_display = (
        catalog.models.Image.image_tmb,
        catalog.models.Image.item.field.name,
    )
