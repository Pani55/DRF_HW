from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from studing.models import Course, Lesson, SubscriptionOnCourse
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="example@example.com")
        self.course = Course.objects.create(title="chepukha", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="ajajaja",
            link="http//youtube.com",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("studing:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.lesson.title)

    def test_lesson_create(self):
        url = reverse("studing:lesson_create")
        data1 = {
            "title": "test_lesson",
            "link": "http://youtube.com",
            "course": self.course.pk,
        }
        response1 = self.client.post(url, data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        data2 = {
            "title": "test_bad_link",
            "link": "http://violenty.ru",
            "course": self.course.pk,
        }
        response2 = self.client.post(url, data2)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse("studing:lesson_update", args=(self.lesson.pk,))
        data = {"title": "test"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "test")

    def test_lesson_delete(self):
        url = reverse("studing:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("studing:lesson_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]), 1)


class SubscriptionOnCourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="example@example.com")
        self.course = Course.objects.create(title="chepukha", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("studing:subscription")
        data = {
            "course": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SubscriptionOnCourse.objects.count(), 1)
        self.assertEqual(response.data.get("message"), "Подписка добавлена")

    def test_subscription_delete(self):
        url = reverse("studing:subscription")
        SubscriptionOnCourse.objects.create(user=self.user, course=self.course)
        data = {
            "course": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubscriptionOnCourse.objects.count(), 0)
        self.assertEqual(response.data.get("message"), "Подписка удалена")
