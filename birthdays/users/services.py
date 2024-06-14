from django.conf import settings
from django.core.mail import EmailMessage


def send_notification(user_email: str, birthday_users_list: list[str]) -> None:
    from_email = settings.DEFAULT_FROM_EMAIL
    birthdays_users_str = ', '.join(birthday_users_list)
    message = (f'Поздравьте сегодняшних именинников: {birthdays_users_str}.'
               f' Им будет приятно')
    email = EmailMessage(
        subject='Сегодня родились и ждут поздравления...',
        body=message,
        from_email=from_email,
        to=user_email
    )
    email.send()


def send_congratulation(user_email: str, message: str) -> None:
    pass
