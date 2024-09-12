from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog.models import Category, Item, Tag

__all__ = []


class StaticURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_catalog_endpoint(self):
        response = self.client.get(reverse("catalog:catalog"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_friday_endpoint(self):
        response = self.client.get(reverse("catalog:friday"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_new_items_endpoint(self):
        response = self.client.get(reverse("catalog:new_items"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unverified_endpoint(self):
        response = self.client.get(reverse("catalog:unverified"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @parameterized.expand(
        [
            ("-1",),
            ("1---",),
            ("1pds",),
            ("pds21",),
            ("pl",),
        ],
    )
    def test_catalog_endpoint_with_wrong_item(self, value):
        response = self.client.get(f"/catalog/{value}/")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class ContextTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.published_category = Category.objects.create(
            is_published=True,
            name="Text published",
            slug="published_category",
            weight=100,
        )
        cls.unpublished_category = Category.objects.create(
            is_published=False,
            name="Text unpublished",
            slug="unpublished_category",
            weight=100,
        )
        cls.published_tag = Tag.objects.create(
            is_published=True,
            name="Text published",
            slug="published_tag",
        )
        cls.unpublished_tag = Tag.objects.create(
            is_published=False,
            name="Text unpublished",
            slug="unpublished_tag",
        )
        cls.published_item = Item.objects.create(
            is_published=True,
            name="Text published",
            text="Text published",
            category=cls.published_category,
        )
        cls.unpublished_item = Item.objects.create(
            is_published=False,
            name="Text unpublished",
            text="Text unpublished",
            category=cls.published_category,
        )

        cls.published_category.clean()
        cls.unpublished_category.clean()
        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.clean()
        cls.unpublished_tag.clean()
        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item.tags.add(cls.published_tag)
        cls.published_item.tags.add(cls.unpublished_tag)

        cls.published_item.clean()
        cls.unpublished_item.clean()
        cls.published_item.save()
        cls.unpublished_item.save()

    def tearDown(self):
        pass

    def test_catalog_show_correct_context(self):
        response = self.client.get(
            reverse(
                "homepage:home",
            ),
        )
        self.assertIn("items", response.context)

    def test_catalog_count_item(self):
        response = self.client.get(reverse("catalog:catalog"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_catalog_item_tags(self):
        response = self.client.get(reverse("catalog:catalog"))
        item = response.context["items"][0]
        self.assertEqual(item.tags.all()[0], self.published_tag)

    def test_catalog_count_item_tags(self):
        response = self.client.get(reverse("catalog:catalog"))
        item = response.context["items"][0]
        count_tags = len(item.tags.all())
        self.assertEqual(count_tags, 1)

    def test_catalog_type(self):
        response = self.client.get(reverse("catalog:catalog"))
        item = response.context["items"][0]
        self.assertIsInstance(item, Item)
        self.assertIsInstance(item.tags.first(), Tag)

    def test_catalog_item_fields(self):
        response = self.client.get(reverse("catalog:catalog"))
        item = response.context["items"][0]
        fields = [
            "name",
            "text",
        ]
        for value in fields:
            self.assertIn(value, item.__dict__)
        self.assertNotIn("is_published", item.__dict__)
        self.assertIn(self.published_tag, item.tags.all())
        self.assertIn("_prefetched_objects_cache", item.__dict__)
