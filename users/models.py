from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=128,
                                blank=False,
                                unique=True,
                                verbose_name="Имя пользователя")
    first_name = models.CharField(
        max_length=128, blank=False, verbose_name="Имя")
    last_name = models.CharField(
        max_length=128, blank=False, verbose_name="Фамилия")
    password = models.CharField(
        max_length=128, blank=False, verbose_name="Пароль")
    email = models.EmailField(
        max_length=128, blank=False, unique=True, verbose_name="e-mail")

    @property
    def is_admin(self):
        return self.is_staff

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} '

    class Meta:
        ordering = ['-pk']
