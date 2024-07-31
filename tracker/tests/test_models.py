from django.test import TestCase
from tracker.models import Click


class ClickModelTest(TestCase):

    def setUp(self):
        self.click = Click.objects.create(
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0",
            project_id="test_project",
            thank_you_page="http://example.com/thank-you"
        )

    # Click test
    def test_click_creation(self):
        self.assertIsInstance(self.click, Click)
        self.assertEqual(self.click.ip_address, "127.0.0.1")
        self.assertEqual(self.click.user_agent, "Mozilla/5.0")
        self.assertEqual(self.click.project_id, "test_project")
        self.assertEqual(self.click.thank_you_page, "http://example.com/thank-you")

    # str test
    def test_click_str_method(self):
        expected_str = f"Click from {self.click.ip_address} at {self.click.timestamp}"
        self.assertEqual(str(self.click), expected_str)
