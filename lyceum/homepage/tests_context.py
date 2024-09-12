from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, Item, Tag

__all__ = []


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
            category=cls.published_category,
        )
        cls.unpublished_item = Item.objects.create(
            is_published=False,
            name="Text unpublished",
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

    def test_home_page_show_correct_context(self):
        response = self.client.get(
            reverse(
                "homepage:home",
            ),
        )
        self.assertIn("items", response.context)

    def test_home_page_count_item(self):
        response = self.client.get(reverse("homepage:home"))
        items = response.context["items"]
        self.assertEqual(items.count(), 1)

    def test_home_page_item_category(self):
        response = self.client.get(reverse("homepage:home"))
        item = response.context["items"][0]
        self.assertEqual(item.category, self.published_category)

    def test_home_page_item_tags(self):
        response = self.client.get(reverse("homepage:home"))
        item = response.context["items"][0]
        self.assertEqual(item.tags.all()[0], self.published_tag)

    def test_home_page_count_item_tags(self):
        response = self.client.get(reverse("homepage:home"))
        item = response.context["items"][0]
        count_tags = item.tags.all().count()
        self.assertEqual(count_tags, 1)
