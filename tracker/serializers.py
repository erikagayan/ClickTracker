from tracker.models import Click
from rest_framework import serializers


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = "__all__"
