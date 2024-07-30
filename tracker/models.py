import string
import random
from django.db import models


class Click(models.Model):
    ip_address = models.GenericIPAddressField(protocol="both")
    user_agent = models.CharField(max_length=256)  # store browser info
    timestamp = models.DateTimeField(auto_now_add=True)  # store click time
    project_id = models.CharField(max_length=100, blank=True, null=True)
    thank_you_page = models.URLField(default="http://example.com/thank-you")

    def __str__(self):
        return f"Click from {self.ip_address} at {self.timestamp}"


class ShortURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    thank_you_page = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super(ShortURL, self).save(*args, **kwargs)

    def generate_short_code(self):
        length = 6
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(length))
            if not ShortURL.objects.filter(short_code=short_code).exists():
                break
        return short_code
