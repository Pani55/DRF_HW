from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment

"""Сериализаторы для пользователей"""

pass


"""Сериализаторы для платежей"""


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
