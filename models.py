

from django.db import models
from django.contrib.auth.models import User

# То что нужно описать
class Player_2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='igrok_1', verbose_name='Пользователь', blank=True, null=True)
    first_enter = models.DateTimeField(verbose_name="Момент первого входа", blank=True, null=True)
    end_enter = models.DateTimeField(verbose_name="Момент последнего входа", blank=True, null=True)
    uroven = models.ForeignKey('Urovni', on_delete=models.SET_NULL, related_name='player_2_urovni',
                                 verbose_name='Уровень пользователя', null=True, blank=True)
    ball_all = models.PositiveIntegerField(verbose_name="Общее Количество баллов", default=0)


# (Повышать)
class Boost(models.Model):
    name = models.CharField(verbose_name="Наименование повышения", max_length=100, null=True, blank=True)
    boost = models.PositiveIntegerField(verbose_name="Количество баллов", default=0)

# Модель уровней написал, помтому, что у уровней могут быть какие то свойства тоже, от которых потом что то может
# зависеть.
class Urovni(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)





