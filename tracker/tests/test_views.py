from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tracker.models import Click
from django.urls import reverse


class ClickViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.click_data = {
            "project_id": "test_project",
            "thank_you_page": "http://example.com/thank-you"
        }
        self.click = Click.objects.create(
            ip_address="192.168.0.1",
            user_agent="Mozilla/5.0",
            project_id="test_project",
            thank_you_page="http://example.com/thank-you"
        )
        self.list_url = reverse('click-list')
        self.redirect_url = reverse('click_redirect', args=[self.click.id])

    def test_create_click(self):
        headers = {
            'REMOTE_ADDR': '192.168.0.1',
            'HTTP_USER_AGENT': 'Mozilla/5.0'
        }
        response = self.client.post(self.list_url, self.click_data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Click.objects.count(), 2)
        self.assertEqual(Click.objects.latest('id').ip_address, '192.168.0.1')
        self.assertEqual(Click.objects.latest('id').user_agent, 'Mozilla/5.0')

    def test_list_clicks(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ip_address'], self.click.ip_address)

    def test_retrieve_click(self):
        url = reverse('click-detail', args=[self.click.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ip_address'], self.click.ip_address)

    def test_redirect_nonexistent_click(self):
        non_existent_redirect_url = reverse('click_redirect', args=[999])
        response = self.client.get(non_existent_redirect_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
