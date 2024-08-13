from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Адрес электронной почты", unique=True)
    phone = models.CharField(
        max_length=35, verbose_name="Номер телефона", blank=True, null=True
    )
    city = models.CharField(max_length=50, verbose_name="Город", blank=True, null=True)
    photo = models.ImageField(
        verbose_name="Фотография профиля", upload_to="users/", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date_of_payment = models.DateTimeField(
        verbose_name="Дата оплаты",
        auto_now_add=True,
    )
    paid_lesson = models.ForeignKey(
        to="studing.Lesson",
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
    )
    paid_course = models.ForeignKey(
        to="studing.Course",
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
    )
    summ_of_payment = models.FloatField(verbose_name="Сумма оплаты")
    method_choices = ((1, "Наличные"), (2, "Перевод на счёт"))
    payment_method = models.IntegerField(
        choices=method_choices, verbose_name="Метод оплаты", blank=True, null=True
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"{self.user} - {self.paid_lesson if self.paid_lesson else self.paid_course}"
