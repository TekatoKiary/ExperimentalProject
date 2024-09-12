from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class StaticURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_endpoint(self):
        response = self.client.get(reverse("about:about"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
