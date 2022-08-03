import datetime
import requests
import xml.etree.ElementTree as ET

from django.core.cache import cache

from deal.models import ValutaRate

CRB_USA_ID = 'R01235'


def get_cbr_exchange_rate(date: datetime.datetime, valuta_id: str) -> float:
    """
    Метод получающий актуальный курс валюты.
    на указанную дату с сайта https://www.cbr.ru/development/SXML/

    :param date: Дата на которую нужно получить курс. День, месяц, год обязательны.
    :param valuta_id: Идентификатор валюты внутри системы центробанка.
    :return: Количество рублей за еденицу валюты.
    """
    date = date.strftime('%d/%m/%Y')
    cbr_api_path_with_date = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url=cbr_api_path_with_date)
    tree = ET.fromstring(response.content)
    elem = tree.find(f".//*[@ID='{valuta_id}']/Value")
    return float(elem.text.replace(',', '.'))


def get_cbr_usa_dollar_exchange_rate(date: datetime.datetime) -> float:
    """
    Курс доллара в заданную дату.

    :param date: Дата на которую нужно получить курс. День, месяц, год обязательны.
    :return: Количество рублей за еденицу валюты.
    """
    rate = get_cbr_exchange_rate(date, CRB_USA_ID)
    return rate


def get_cbr_today_exchange_rate(valuta_id: str) -> float:
    """
    Курс валюты за сегодня.

    :param valuta_id: Идентификатор валюты внутри системы центробанка.
    :return: Количество рублей за еденицу валюты.
    """
    date = datetime.datetime.now()
    rate = get_cbr_exchange_rate(date, valuta_id)
    return rate


def get_usa_dollar_today_exchange_rate() -> float:
    """
    Курс доллара за сегодня.

    :return: Количество рублей за еденицу валюты.
    """
    return get_cbr_today_exchange_rate(CRB_USA_ID)


def get_actual_valuta_rate():
    """Функция получает курс доллара, сохраняет его в базу и кэш"""
    rate = get_usa_dollar_today_exchange_rate()
    cache.set('usa_rate', rate, 60 * 60)
    return rate


if __name__ == "__main__":
    date = datetime.datetime.now()
    print(get_cbr_usa_dollar_exchange_rate(date))
