from celery import shared_task
from django.utils import timezone

from .models import User
from .services import send_notification, send_congratulation
from birthdays.celery import app


@shared_task
def check_birthday_users_task():
    current_date = timezone.now().date()
    users_for_sending_notifications = User.objects.exclude(
        is_notification_agree=False)
    for user in users_for_sending_notifications:
        users_birthday_today_and_follow = [
            user.first_name + ' ' + user.last_name for user in
            User.objects.prefetch_related(
                'follower',
                'following'
            ).filter(
                birth_date__day=current_date.day,
                birth_date__month=current_date.month
            ).filter(following__user=user)]
        if users_birthday_today_and_follow:
            send_notification(user.email, users_birthday_today_and_follow)


@app.task
def send_congratulation_task(user_email, message):
    send_congratulation(user_email, message)
