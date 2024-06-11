from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(verbose_name='Имя', max_length=150)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    surname = models.CharField(verbose_name='Отчество', max_length=150,
                               blank=True)
    birth_date = models.DateField(verbose_name='Дата рождения')
    is_notification_agree = models.BooleanField(default=True)
    email = models.EmailField(verbose_name='Электронная почта',
                              blank=False, null=False)

    REQUIRED_FIELDS = ['email', 'birth_date']

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_cannot_follow_yourself'
            ),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'
            )
        ]
        verbose_name = 'Подписка',
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
