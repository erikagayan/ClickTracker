from rest_framework import serializers
from tracker.models import Click, ShortURL


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = "__all__"


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_code', 'thank_you_page']
        read_only_fields = ['short_code']
