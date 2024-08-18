from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializeers import UserSerializer
from users.serializers import PaymentSerializer


# Create your views here.
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ["paid_lesson", "paid_course", "payment_method"]
    serializer_class = PaymentSerializer
    ordering_fields = ["date_of_payment"]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
