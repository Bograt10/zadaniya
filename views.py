from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
import datetime
from django.core.cache import cache

from test_1.models import *
from proect.selery import app

# Create your views here.


class Zadanie_1_View(LoginRequiredMixin, View):
    model = User
    template_name = "test_1/zadanie_1/zadanie_1.html"

    def get(self, request, *args, **kwargs):
        # Получим пользователя
        polzovatel = self.request.user
        current_time = datetime.datetime.now().astimezone()
        # Запросим информацию из кэша , о том заходил ли пользователь в игру за последние сутки
        vhod = cache.get(f'{polzovatel.pk}_Zadanie_1_View_vhod')
        # Если заходил
        if vhod:
            pass
        else:
            # Вызовем таску в которой обработаем вариант с первым входом пользователя, и начислением бонусов ему за
            # последовательный вход раз в сутки.
            Task_1.delay(polzovatel.pk)
            # Создадим кэш который будет отмечать пользователя который заходил в игру, и хранить информацию об его входе
            # сутки
            vhod = f'{polzovatel.pk}_Zadanie_1_View_vhod'
            cache.set(vhod, current_time, ((60 * 60) * 24))

        slovar_itog = {}

        return render(request, self.template_name, slovar_itog)


@app.task
def Task_1(uzer_pk):
        from django.contrib.auth.models import User
        from test_1.models import Player_2, Boost, Urovni


        user_1 = User.objects.get(pk=uzer_pk)
        current_time = datetime.datetime.now().astimezone()
        # С начало проверим входил ли хоть раз пользователь в систему
        vhod_1 = Player_2.objects.filter(user__pk=uzer_pk).exists()
        # Если пользователь уже входил в игру
        if vhod_1:
            igrok = Player_2.objects.get(user__pk=uzer_pk)
            if igrok.end_enter:
                # Проверим входил ли пользователь в игру в течении последних суток
                vhod_posledn = current_time - igrok.end_enter
                # Бонус начисляется игроку если он заходил в промежутке между 1 и вторыми сутками
                znazenie_1 = 1 if vhod_posledn.days < 2 else None
                print(znazenie_1)
                if znazenie_1:
                    # Получим в таблице бустов количество баллов которое начисляется за 1 вход в течении каждых суток
                    bonus = Boost.objects.get(pk=3)
                    # Добавим бонусы игроку
                    igrok.ball_all = igrok.ball_all + bonus.boost
                    igrok.save()
                # Перезапишем дату последнего входа в игру
                igrok.end_enter = current_time
                igrok.save()


        # Если пользователь не входил ранее в игру.
        else:
            # Возьмем из таблицы бонусов объект который начисляет определенное количество бонусов за первое вхождение
            # в игру.
            bonus = Boost.objects.get(pk=1)
            # Получим нулевой уровень из таблицы уровней.
            uroven = Urovni.objects.get(pk=4)
            # Заполним данны
            obj_1 = Player_2.objects.create(user=user_1, first_enter=current_time, end_enter=current_time,
                                            uroven=uroven, ball_all=bonus.boost)
            obj_1.save()
            print(obj_1)







