from django.test import TestCase, Client

from http import HTTPStatus


class AboutUrlsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.urls_names_template = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html'
        }

    def testing_urls_exists(self):
        """Тест URL-адреса на наличие их в коде."""
        for urls_address in self.urls_names_template:
            with self.subTest(urls_address):
                response = self.guest_client.get(urls_address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def testing_urls_correct_templates(self):
        """Тест URL-адреса используются ли верные шаблоны."""
        for url, template in self.urls_names_template.items():
            with self.subTest(template=template):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
