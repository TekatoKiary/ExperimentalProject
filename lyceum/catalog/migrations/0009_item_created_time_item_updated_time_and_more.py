# Generated by Django 4.2 on 2023-11-03 22:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "catalog",
            "0008_alter_item_options_remove_item_images_image_item_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="created_time",
            field=models.DateTimeField(
                auto_created=True,
                auto_now_add=True,
                null=True,
                verbose_name="Дата создания",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="updated_time",
            field=models.DateTimeField(
                auto_now=True, null=True, verbose_name="Дата изменения"
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(
                upload_to="catalog/images/%Y/%m/%d/",
                verbose_name="Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="mainimage",
            name="image",
            field=models.ImageField(
                upload_to="catalog/main_images/", verbose_name="Изображение"
            ),
        ),
    ]
