import datetime

import django.db.models
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from catalog.models import Image, Item, Tag

__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = Item.objects.published()

    context = {"items": items}
    return render(request, template, context)


def new_items(request):
    template = "catalog/item_list.html"
    date_now = now()
    date_last_now = date_now - datetime.timedelta(days=7)
    items = (
        Item.objects.filter(
            is_published=True,
            category__is_published=True,
            created_time__range=(date_last_now, date_now),
        )
        .select_related(
            Item.category.field.name,
            Item.main_image.field.name,
        )
        .prefetch_related(
            django.db.models.Prefetch(
                Item.tags.field.name,
                queryset=Tag.objects.filter(is_published=True).only(
                    Tag.name.field.name,
                ),
            ),
        )
        .only(
            Item.name.field.name,
            Item.text.field.name,
            "category__name",
            Item.main_image.field.name,
        )
        .order_by(
            "category__name",
            Item.name.field.name,
        )
    )
    context = {
        "items": items,
        "title": "Новинки",
    }
    return render(request, template, context)


def friday_items(request):
    template = "catalog/item_list.html"
    friday_id = 5
    items = (
        Item.objects.filter(
            is_published=True,
            category__is_published=True,
            updated_time__iso_week_day__exact=friday_id,
        )
        .select_related(
            Item.category.field.name,
            Item.main_image.field.name,
        )
        .prefetch_related(
            django.db.models.Prefetch(
                Item.tags.field.name,
                queryset=Tag.objects.filter(is_published=True).only(
                    Tag.name.field.name,
                ),
            ),
        )
        .only(
            Item.name.field.name,
            Item.text.field.name,
            "category__name",
            Item.main_image.field.name,
        )
        .order_by(
            "category__name",
            Item.name.field.name,
        )
    )
    context = {
        "items": items,
        "title": "Пятница",
    }
    return render(request, template, context)


def unverified(request):
    template = "catalog/item_list.html"
    items = (
        Item.objects.filter(
            is_published=True,
            category__is_published=True,
            updated_time=None,
        )
        .select_related(
            Item.category.field.name,
            Item.main_image.field.name,
        )
        .prefetch_related(
            django.db.models.Prefetch(
                Item.tags.field.name,
                queryset=Tag.objects.filter(is_published=True).only(
                    Tag.name.field.name,
                ),
            ),
        )
        .only(
            Item.name.field.name,
            Item.text.field.name,
            "category__name",
            Item.main_image.field.name,
        )
        .order_by(
            "category__name",
            Item.name.field.name,
        )
    )
    context = {
        "items": items,
        "title": "Непроверенное",
    }
    return render(request, template, context)


def item_detail(request, item):
    item_object = get_object_or_404(
        Item.objects.filter(id=item)
        .select_related(
            Item.category.field.name,
            Item.main_image.field.name,
        )
        .prefetch_related(
            django.db.models.Prefetch(
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
            "category__name",
            Item.main_image.field.name,
        ),
    )
    images = Image.objects.filter(item__id=item).only(Image.image.field.name)
    template = "catalog/item_detail.html"
    context = {"item": item_object, "images": images}
    return render(request, template, context)
