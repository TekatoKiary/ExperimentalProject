from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_endpoint(self):
        response = Client().get("/catalog/1/")
        self.assertEqual(response.status_code, 200)

    def test_wrong_catalog_item_endpoint(self):
        response = Client().get("/catalog/pl/")
        self.assertEqual(response.status_code, 404)
