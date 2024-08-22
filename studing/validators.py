from rest_framework import serializers

allowed_links = "youtube.com"


def validate_allowed_links(value):
    if allowed_links not in value:
        raise serializers.ValidationError("Доступны лишь ссылки на YouTube!")
