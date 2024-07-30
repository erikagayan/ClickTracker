from django.db import models


class Click(models.Model):
    ip_address = models.GenericIPAddressField(protocol="both")
    user_agent = models.CharField(max_length=256)  # store browser info
    timestamp = models.DateTimeField(auto_now_add=True)  # store click time
    project_id = models.CharField(max_length=100, blank=True, null=True)
    thank_you_page = models.URLField(default="http://example.com/thank-you")

    def __str__(self):
        return f"Click from {self.ip_address} at {self.timestamp}"
