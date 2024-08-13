from django.contrib import admin

from users.models import Payment, User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone", "city", "is_staff", "is_superuser")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date_of_payment",
        "paid_lesson",
        "paid_course",
        "summ_of_payment",
        "payment_method",
    )
