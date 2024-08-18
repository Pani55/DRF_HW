from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="course/preview", verbose_name="Превью курса", blank=True, null=True
    )
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    preview = models.ImageField(
        upload_to="lesson/preview", verbose_name="Превью урока", blank=True, null=True
    )
    link = models.TextField(
        verbose_name="Ссылка на урок",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Владелец урока",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
