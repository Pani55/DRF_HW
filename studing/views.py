from rest_framework import status, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from studing.models import Course, Lesson, SubscriptionOnCourse
from studing.paginations import CustomPagination
from studing.serializers import (CourseSerializer, LessonSerializer,
                                 SubscriptionSerializer)
from users.permissions import IsModer, IsOwner
from users.services import create_stripe_product
from studing.tasks import send_subscription_notification


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        stripe_product_id = create_stripe_product(course.title)
        serializer.save(owner=self.request.user, stripe_product_id=stripe_product_id)

    def perform_update(self, serializer):
        course = serializer.save()
        result = send_subscription_notification.delay(course_id=course.pk)
        result.get()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                ~IsModer,
                IsOwner,
            )
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        stripe_product_id = create_stripe_product(lesson.title)
        serializer.save(owner=self.request.user, stripe_product_id=stripe_product_id)

    def get_permissions(self):
        self.permission_classes = (
            IsAuthenticated,
            ~IsModer,
        )
        return super().get_permissions()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (
            IsAuthenticated,
            IsOwner | IsModer,
        )
        return super().get_permissions()


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (
            IsAuthenticated,
            IsOwner | IsModer,
        )
        return super().get_permissions()


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        self.permission_classes = (
            IsAuthenticated,
            ~IsModer | IsOwner,
        )
        return super().get_permissions()


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = SubscriptionOnCourse.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            data = {"message": message, "subscription": "Объект удален"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            subscription = SubscriptionOnCourse.objects.create(
                user=user, course=course_item
            )
            message = "Подписка добавлена"
            subscription = SubscriptionSerializer().to_representation(subscription)
            data = {"message": message, "subscription": subscription}
            return Response(data, status=status.HTTP_201_CREATED)
