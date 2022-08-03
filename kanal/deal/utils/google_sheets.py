from datetime import datetime

import gspread
from celery.utils.log import get_task_logger
from django.core.cache import cache

from deal.models import Deal
from deal.utils.cbr_exchange_rate import get_actual_valuta_rate

logger = get_task_logger(__name__)


def get_data_from_google_sheet(key_filename: str, sheet_name: str):
    """
    Получет данные из гугл таблицы.
    Получает курс дллара из кэша, если кэш пустой
    то из базы и запускает задачу на обновление курса.
    """
    gc = gspread.service_account(filename=key_filename)
    sh = gc.open(sheet_name)
    sheet_data = sh.sheet1.get_all_values()
    logger.info(sh.sheet1.get_all_values())
    dollar_rate = cache.get('usa_rate')
    if not dollar_rate:
        dollar_rate = get_actual_valuta_rate()
    order_id_list = [line[1] for line in sheet_data[1:]]
    obj_list = [
        Deal(
            table_id=line[0],
            order_id=line[1],
            usa_dollar_price=int(line[2]),
            ruble_price=int(line[2]) * dollar_rate,
            delivery_time=datetime.strptime(line[3], '%d.%m.%Y'),
        )
        for line in sheet_data[1:]
    ]
    Deal.objects.bulk_update_or_create(
        obj_list,
        ['table_id', 'usa_dollar_price', 'ruble_price', 'delivery_time'],
        match_field='order_id'
    )
    Deal.objects.exclude(order_id__in=order_id_list).delete()
