from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from studing.models import Course, Lesson, SubscriptionOnCourse
from studing.validators import validate_allowed_links

"""Сериализатор уроков"""


class LessonSerializer(ModelSerializer):
    link = serializers.CharField(validators=[validate_allowed_links])

    class Meta:
        model = Lesson
        fields = "__all__"


"""Сериализатор курсов"""


class CourseSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_subscription(self, obj):
        try:
            subscription = SubscriptionOnCourse.objects.get(course=obj, user=self.context["request"].user)
            return SubscriptionSerializer(subscription).data
        except SubscriptionOnCourse.DoesNotExist:
            return None

    class Meta:
        model = Course
        fields = "__all__"


"""Сериализатор подписок"""


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = SubscriptionOnCourse
        fields = "__all__"
