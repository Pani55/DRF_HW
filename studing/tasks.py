from celery import shared_task
from django.core.mail import send_mail

from config import settings
from studing.models import Course, SubscriptionOnCourse


@shared_task
def send_subscription_notification(course_id):
    course_item = Course.objects.get(pk=course_id)
    subs_items = SubscriptionOnCourse.objects.filter(course=course_item, is_active=True)

    for subs_item in subs_items:
        subject = f"Обновление курса: {course_item.title}"
        message = (f"Привет, {subs_item.user.email}! Курс,"
                   f" на который вы подписаны:'{course_item.title}', получил обновки!")
        recipient_list = [subs_item.user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
