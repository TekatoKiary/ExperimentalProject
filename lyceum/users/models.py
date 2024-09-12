from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birthday = models.DateField(
        "Дата рождения",
        blank=True,
        null=True,
    )

    image = models.ImageField(
        "Аватарка",
        upload_to="users/profile_images/",
        blank=True,
        null=True,
    )

    coffee_count = models.PositiveIntegerField(
        "Количество сваренных кофе",
        default=0,
    )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"
