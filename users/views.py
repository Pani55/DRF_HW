from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_stripe_price, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.paid_course:
            obj = payment.paid_course
        else:
            obj = payment.paid_lesson
        price = create_stripe_price(obj)
        session_id, link_for_payment = create_stripe_session(price)
        payment.link = link_for_payment
        payment.session_id = session_id
        payment.save()
