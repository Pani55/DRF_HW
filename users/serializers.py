from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User

"""Сериализаторы для пользователей"""


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


"""Сериализаторы для платежей"""


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
