from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tracker.models import ShortURL
from django.urls import reverse


class ShortURLTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_url = "https://www.google.com"
        self.thank_you_url = "https://www.example.com/thank-you"
        self.short_url_data = {
            "original_url": self.valid_url
        }
        self.short_url = ShortURL.objects.create(original_url=self.valid_url, short_code="test123")

    def test_create_short_url(self):
        response = self.client.post(reverse('shorturl-list'), self.short_url_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_code', response.data)
        self.assertIn('original_url', response.data)
        self.assertEqual(response.data['original_url'], self.valid_url)

    def test_redirect_to_original_url(self):
        response = self.client.get(reverse('redirect_to_original', args=[self.short_url.short_code]), follow=False)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response['Location'], self.valid_url)

    def test_redirect_to_thank_you_page(self):
        self.short_url.thank_you_page = self.thank_you_url
        self.short_url.save()
        response = self.client.get(reverse('redirect_to_original', args=[self.short_url.short_code]), follow=False)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response['Location'], self.thank_you_url)

    def test_redirect_nonexistent_short_url(self):
        response = self.client.get(reverse('redirect_to_original', args=['nonexistent']), follow=False)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_thank_you_page(self):
        response = self.client.patch(reverse('shorturl-detail', args=[self.short_url.id]) + 'update_thank_you_page/', {'thank_you_page': self.thank_you_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.short_url.refresh_from_db()
        self.assertEqual(self.short_url.thank_you_page, self.thank_you_url)
