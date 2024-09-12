from http import HTTPStatus
from pathlib import Path
import tempfile

from django.conf import settings
from django.core.files.base import ContentFile
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from parameterized import parameterized

from feedback.forms import AuthorForm, FeedbackForm, FileForm
from feedback.models import Author, Feedback, FeedbackFile

__all__ = []


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.feedback_form = FeedbackForm()
        cls.user_form = AuthorForm()
        cls.file_form = FileForm()

    def tearDown(self):
        pass

    def test_labels(self):
        name_label = self.user_form.fields["name"].label
        mail_label = self.user_form.fields["mail"].label
        text_label = self.feedback_form.fields["text"].label
        file_label = self.file_form.fields["file"].label
        self.assertEqual(mail_label, "Электронная почта")
        self.assertEqual(name_label, "Имя")
        self.assertEqual(text_label, "Отзыв")
        self.assertEqual(file_label, "Файлы")

    def test_help_texts(self):
        name_label = self.user_form.fields["name"].help_text
        mail_label = self.user_form.fields["mail"].help_text
        text_label = self.feedback_form.fields["text"].help_text
        self.assertEqual(mail_label, "Напишите Вашу электронную почту")
        self.assertEqual(text_label, "Напишите Ваш отзыв")
        self.assertEqual(name_label, "Введите Ваше имя")

    def test_create_feedback(self):
        feedback_count = Feedback.objects.count()
        form_data = {
            "mail": "example@example.com",
            "text": "Test",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(Feedback.objects.count(), feedback_count + 1)
        self.assertTrue(Feedback.objects.filter(text="Test").exists())
        self.assertWarnsMessage(response, "Форма успешно отправлена")

    def test_get_method(self):
        response = Client().get(
            reverse("feedback:feedback"),
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.expand(
        [
            ("example@example.com", "Test_user", True),
            ("example", "test_user", False),
        ],
    )
    def test_user_form(self, mail, name_user, is_valid):
        user_count = Author.objects.count()
        form_data = {"mail": mail, "name": name_user}
        form = AuthorForm(data=form_data)
        self.assertEqual(form.is_valid(), is_valid)
        if not is_valid:
            self.assertFormError(
                form,
                "mail",
                ["Введите правильный адрес электронной почты."],
            )
            self.assertEqual(user_count, Author.objects.count())

    @override_settings(MEDIA_ROOT=tempfile.TemporaryDirectory().name)
    def test_upload_files_in_form(self):
        files = [
            ContentFile(
                f"file_{index}".encode(),
                name="filename",
            )
            for index in range(10)
        ]
        data = {
            "text": "Test",
            "mail": "example@mail.com",
            "name": "Test Name",
            "file": files,
        }
        response = Client().post(
            reverse("feedback:feedback"),
            data=data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(FeedbackFile.objects.count(), len(files))

        media_root = Path(settings.MEDIA_ROOT)

        for index, file in enumerate(FeedbackFile.objects.all()):
            uploaded_file = media_root / file.file.path
            self.assertEqual(
                uploaded_file.open().read(),
                f"file_{index}",
            )
