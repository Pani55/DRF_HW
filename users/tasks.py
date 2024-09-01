from datetime import timedelta, datetime
from pytz import timezone
from celery import shared_task

from config import settings
from users.models import User


@shared_task
def check_last_login__disactivate_user():
    """
    Задача для автоматического деактивации пользователей,
    которые не авторизовались в системе более 30 дней назад.
    """
    now = datetime.now(timezone(settings.TIME_ZONE))
    threshold_date = now - timedelta(days=30)
    active_users = User.objects.filter(last_login__gte=threshold_date, is_active=True)

    for user in active_users:
        user.is_active = False
        user.save()
