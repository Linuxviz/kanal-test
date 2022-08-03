import datetime

import telebot

from deal.models import Deal


def init_bot():
    bot = telebot.TeleBot('5522956486:AAEr1x-3uAGuclUJ28PAXx7JgYKzWdeEta8')

    @bot.message_handler(commands=["start"])
    def start(message, res=False):
        bot.send_message(
            message.chat.id,
            'Я на связи, напишите "пп" что бы увидеть информацию о прошедших поставках, '
            '"бп" - о будущих.'
        )

    # Получение сообщений от юзера
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        time = datetime.datetime.now()
        if message.text.lower() == "пп":
            deals = Deal.objects.filter(delivery_time__lt=time)
            result_message = ""
            for deal in deals:
                string = f"{deal.order_id}, {deal.usa_dollar_price}," \
                         f" {deal.ruble_price}, {deal.delivery_time.strftime('%d/%m/%Y')}\n"
                result_message += string
            bot.send_message(message.chat.id, result_message)
        elif message.text.lower() == "бп":
            deals = Deal.objects.filter(delivery_time__gt=time)
            result_message = ""
            for deal in deals:
                string = f"{deal.order_id}, {deal.usa_dollar_price}," \
                         f" {deal.ruble_price}, {deal.delivery_time.strftime('%d/%m/%Y')}\n"
                result_message += string
            bot.send_message(message.chat.id, result_message)
        else:
            bot.send_message(message.chat.id, 'Я вас не понял: ' + message.text)

    bot.infinity_polling()
