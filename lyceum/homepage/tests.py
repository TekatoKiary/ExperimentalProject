from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog.models import Category, Item, Tag

__all__ = []


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.published_category = Category.objects.create(
            is_published=True,
            name="Test home category",
            slug="home_category",
            weight=100,
        )
        cls.published_tag = Tag.objects.create(
            is_published=True,
            name="Test home tag",
            slug="home_tag",
        )

        cls.published_item = Item.objects.create(
            is_published=True,
            name="Text",
            category=cls.published_category,
        )

        cls.published_category.clean()
        cls.published_category.save()

        cls.published_tag.clean()
        cls.published_tag.save()

        cls.published_item.tags.add(cls.published_tag)

        cls.published_item.clean()
        cls.published_item.save()

    def tearDown(self):
        pass

    @parameterized.expand(
        [
            (reverse("homepage:home"), HTTPStatus.OK),
            ("/coffee/", HTTPStatus.IM_A_TEAPOT),
        ],
    )
    def test_endpoints(self, url_path, http_status):
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, http_status)

    @parameterized.expand(
        [
            ("/coffee/", "Я чайник", HTTPStatus.IM_A_TEAPOT),
        ],
    )
    def test_coffee_text(self, url_path, expected_text, http_status):
        response = self.client.get(url_path)
        self.assertContains(response, expected_text, status_code=http_status)
