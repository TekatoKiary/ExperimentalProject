# Generated by Django 4.2 on 2023-10-24 16:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_category_normalize_name_tag_normalize_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="MainImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="catalog/", verbose_name="Изображение"
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение",
                "verbose_name_plural": "изображения",
            },
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Напишите слаг",
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(200)],
                verbose_name="Слаг",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                help_text="Напишите слаг",
                unique=True,
                validators=[django.core.validators.MaxLengthValidator(200)],
                verbose_name="Слаг",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="images",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="catalog.mainimage",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="main_image",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="main_image",
                to="catalog.mainimage",
            ),
        ),
    ]
