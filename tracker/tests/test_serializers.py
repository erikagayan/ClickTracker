from django.test import TestCase
from tracker.models import Click
from tracker.serializers import ClickSerializer
from rest_framework.exceptions import ValidationError


class ClickSerializerTest(TestCase):

    def setUp(self):
        self.click_attributes = {
            "ip_address": "192.168.0.1",
            "user_agent": "Mozilla/5.0",
            "project_id": "test_project",
            "thank_you_page": "http://example.com/thank-you"
        }

        self.serializer_data = {
            "ip_address": "192.168.0.1",
            "user_agent": "Mozilla/5.0",
            "project_id": "test_project",
            "thank_you_page": "http://example.com/thank-you"
        }

        self.click = Click.objects.create(**self.click_attributes)
        self.serializer = ClickSerializer(instance=self.click)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ["id", "ip_address", "user_agent", "timestamp", "project_id", "thank_you_page"])

    def test_ip_address_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["ip_address"], self.click.ip_address)

    def test_user_agent_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["user_agent"], self.click.user_agent)

    def test_project_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["project_id"], self.click.project_id)

    def test_thank_you_page_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["thank_you_page"], self.click.thank_you_page)

    def test_create_valid_click(self):
        serializer = ClickSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        click = serializer.save()
        self.assertEqual(click.ip_address, self.serializer_data["ip_address"])
        self.assertEqual(click.user_agent, self.serializer_data["user_agent"])
        self.assertEqual(click.project_id, self.serializer_data["project_id"])
        self.assertEqual(click.thank_you_page, self.serializer_data["thank_you_page"])

    def test_create_invalid_click(self):
        invalid_data = self.serializer_data.copy()
        invalid_data["ip_address"] = "invalid_ip"
        serializer = ClickSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
