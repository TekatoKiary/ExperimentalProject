from django.urls import path, register_converter

from catalog import converters, views

register_converter(converters.PositiveIntegerConverter, "int")

app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="catalog"),
    path("<int:item>/", views.item_detail, name="catalog_item"),
    path("new/", views.new_items, name="new_items"),
    path("friday/", views.friday_items, name="friday"),
    path("unverified/", views.unverified, name="unverified"),
]
