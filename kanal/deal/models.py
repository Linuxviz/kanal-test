import datetime

from django.db import models  # for hints
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db.models import Model, IntegerField, DateTimeField, FloatField, CharField


class Deal(Model):
    """
    Модель сделки соответствующая гугл таблице.
    """
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    table_id = IntegerField(default=1)  # номер записи
    order_id = IntegerField(default=1)  # номер заказа
    usa_dollar_price = IntegerField(default=1)  # стоимость сделки в долларах
    ruble_price = IntegerField(default=1)  # стоимость сделки в рублях
    delivery_time = DateTimeField(default=datetime.datetime.now())  # срок доставки

    def __str__(self):
        return f"dj_id:{self.pk}, table_id:{self.table_id}," \
               f" order_id:{self.order_id}, usa_dollar_price:{self.usa_dollar_price}," \
               f"  ruble_price:{self.ruble_price}, delivery_time:{self.delivery_time}"


class ValutaRate(Model):
    """
    Курс вылюты сохраненны после последнего сохранения, берется в случае протухания кэша,
    что бы не ждать завершение обновления
    """
    USA_DOLLAR = 'FR'

    VALUTA_CHOICES = [
        (USA_DOLLAR, 'USA_dollar'),
    ]

    name = CharField(max_length=120, choices=VALUTA_CHOICES)
    rate = FloatField()
