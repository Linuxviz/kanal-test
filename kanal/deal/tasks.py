from celery import shared_task
from celery.signals import celeryd_after_setup
from celery.utils.log import get_task_logger

from core import app
from deal.utils.cbr_exchange_rate import get_actual_valuta_rate
from deal.utils.delivey_time_bot import init_bot
from deal.utils.google_sheets import get_data_from_google_sheet

logger = get_task_logger(__name__)


@shared_task
def get_data_from_google_sheet_task():
    """ Забирает данные из гугл таблицы и обновляет состояние базы"""
    get_data_from_google_sheet('deal/utils/orbital-wharf-357912-409a4c71d691.json', 'test')


@app.task
def delivery_time_task():
    """ Запусает "pool" телеграм бота в отдельной задаче. """
    init_bot()


@app.task(bind=True, name="get_option")
def get_valuta_rate_task():
    """ Получает данные об актуальной валюте (курс доллара) на текущий момент, обновляет кэш и базу. """
    get_actual_valuta_rate()


@celeryd_after_setup.connect
def celeryd_after_setup(*args, **kwargs):
    """
    Стартует после запуска селери.
    Используется для запуска задач, которые должны быть запущены один раз:
     - Запуск бота
    """
    delivery_time_task.apply_async(countdown=1 * 20)
