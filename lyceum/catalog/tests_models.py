import django.core
from django.test import TestCase
from parameterized import parameterized

from catalog.models import Category, Item, Tag

__all__ = []


class ModelsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            id=12,
            is_published=True,
            name="Test name",
            slug="test-category-slug",
            weight=100,
        )
        cls.tag = Tag.objects.create(
            id=13,
            is_published=True,
            name="Test name",
            slug="test-tag-slug",
        )
        cls.category.full_clean()
        cls.category.save()
        cls.tag.full_clean()
        cls.tag.save()

    def tearDown(self):
        pass

    def test_unable_create_item_without_must_contain(self):
        item_count = Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            item = Item(name="Test item", category=self.category, text="1")
            item.full_clean()
            item.save()
            item.tags.add(self.tag)
        self.assertEqual(Item.objects.count(), item_count)

    def test_unable_create_item_with_over_max_length_name(self):
        item_count = Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            item = Item(name="T" * 300, category=self.category, text="1")
            item.full_clean()
            item.save()
            item.tags.add(self.tag)
        self.assertEqual(Item.objects.count(), item_count)

    def test_create_item(self):
        item_count = Item.objects.count()
        item = Item(name="Test item", category=self.category, text="роскошно")
        item.full_clean()
        item.save()
        item.tags.add(self.tag)

        self.assertEqual(Item.objects.count(), item_count + 1)

    def test_create_tag(self):
        tag_count = Tag.objects.count()
        tag = Tag(
            is_published=True,
            name="New test tag",
            slug="test-new_tag-slug",
        )
        tag.full_clean()
        tag.save()

        self.assertEqual(Tag.objects.count(), tag_count + 1)

    def test_unable_create_tag_with_over_max_length_slug(self):
        tag_count = Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            tag = Tag(
                is_published=True,
                name="Test tag",
                slug="t" * 300,
            )
            tag.full_clean()
            tag.save()

        self.assertEqual(Tag.objects.count(), tag_count)

    def test_create_category(self):
        category_count = Category.objects.count()
        category = Category(
            is_published=True,
            name="New test category",
            slug="test-new_category-slug",
            weight=100,
        )
        category.full_clean()
        category.save()

        self.assertEqual(Category.objects.count(), category_count + 1)

    def test_unable_create_category_with_over_max_length_slug(self):
        category_count = Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            category = Category(
                is_published=True,
                name="Test category",
                slug="t" * 300,
                weight=100,
            )
            category.full_clean()
            category.save()

        self.assertEqual(Category.objects.count(), category_count)

    @parameterized.expand([(-1,), (32768,)])
    def test_unable_create_category_with_wrong_weight(self, value):
        category_count = Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            category = Category(
                is_published=True,
                name="1" * 201,
                slug="test-new_category-slug",
                weight=value,
            )
            category.full_clean()
            category.save()

        self.assertEqual(Category.objects.count(), category_count)

    @parameterized.expand(
        [
            ("test name"),
            ("test nаmе"),
            ("test, nаmе"),
            ("tesT, nаmе"),
            ("tesT,      nаmе"),
            ("tesT, nаmе    "),
            ("    tesT, nаmе"),
        ],
    )
    def test_unable_create_category_with_same_name(self, value):
        category_count = Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            category = Category(
                is_published=True,
                name=value,
                slug="test-new_category-slug",
                weight=1,
            )
            category.full_clean()
            category.save()
        self.assertEqual(Category.objects.count(), category_count)

    @parameterized.expand(
        [
            ("test name"),
            ("test nаmе"),
            ("test, nаmе"),
            ("tesT, nаmе"),
            ("tesT,      nаmе"),
            ("tesT, nаmе    "),
            ("    tesT, nаmе"),
        ],
    )
    def test_unable_create_tag_with_same_name(self, value):
        tag_count = Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            tag = Tag(
                is_published=True,
                name=value,
                slug="test-new_tag-slug",
            )
            tag.full_clean()
            tag.save()

        self.assertEqual(Tag.objects.count(), tag_count)
