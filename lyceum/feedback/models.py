from django.conf import settings
from django.db import models

__all__ = []

STATUS_CHOICES = [
    ("UPD", "в обработке"),
    ("GET", "получено"),
    ("OK", "ответ дан"),
]


class Feedback(models.Model):
    text = models.TextField(
        "Отзыв",
        help_text="Напишите Ваш отзыв",
    )

    created_on = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
        auto_created=True,
    )

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=15,
        default="GET",
    )

    class Meta:
        verbose_name = "письмо обратной связи"
        verbose_name_plural = "письма обратной связи"


class Author(models.Model):
    mail = models.EmailField(
        "Электронная почта",
        help_text="Напишите Вашу электронную почту",
    )
    name = models.CharField(
        "Имя",
        max_length=100,
        help_text="Введите Ваше имя",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name if self.name else "None"

    class Meta:
        verbose_name = "автор обратной связи"
        verbose_name_plural = "авторы обратной связи"

    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        default=None,
    )


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    from_status = models.CharField(
        db_column="from",
        verbose_name="from",
        choices=STATUS_CHOICES,
        max_length=15,
    )
    to = models.CharField(
        db_column="to",
        verbose_name="to",
        choices=STATUS_CHOICES,
        max_length=15,
    )


class FeedbackFile(models.Model):
    def get_path(self, file_name):
        return f"uploads/{self.feedback_id}/{file_name}"

    file = models.FileField(
        "Файлы",
        upload_to=get_path,
        null=True,
        blank=True,
    )
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
