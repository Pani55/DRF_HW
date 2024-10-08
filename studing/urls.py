from django.urls import include, path
from rest_framework.routers import SimpleRouter

from studing.apps import StudingConfig
from studing.views import (CourseViewSet, LessonCreateApiView,
                           LessonDestroyApiView, LessonListApiView,
                           LessonRetrieveApiView, LessonUpdateApiView,
                           SubscriptionAPIView)

app_name = StudingConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lesson_delete"
    ),
    path(
        "lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
    path("subscription/", SubscriptionAPIView.as_view(), name="subscription"),
]

urlpatterns += router.urls
