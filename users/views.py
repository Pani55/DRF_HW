from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from users.models import Payment
from users.serializers import PaymentSerializer


# Create your views here.
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ["paid_lesson", "paid_course", "payment_method"]
    serializer_class = PaymentSerializer
    ordering_fields = ["date_of_payment"]
