from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.urls import reverse

__all__ = []


class StaticURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_words_enabled(self):
        for i in range(1, 31):
            result = "Я кинйач" if i % 10 == 0 else "Я чайник"
            response = self.client.get(reverse("homepage:coffee"))
            self.assertContains(
                response,
                result,
                status_code=HTTPStatus.IM_A_TEAPOT,
            )

    @override_settings(ALLOW_REVERSE=False)
    def test_reverse_words_disabled(self):
        for i in range(10):
            response = self.client.get(reverse("homepage:coffee"))
            self.assertContains(
                response,
                "Я чайник",
                status_code=HTTPStatus.IM_A_TEAPOT,
            )
