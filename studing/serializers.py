from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from studing.models import Course, Lesson

"""Сериализаторы урока"""


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


"""Сериализаторы курса"""


class CourseSerializer(ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
