# Generated by Django 4.2 on 2023-10-31 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_image_alter_mainimage_options_remove_item_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="images",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="catalog.image",
            ),
        ),
    ]
