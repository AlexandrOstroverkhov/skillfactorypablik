import telebot
from config import TOKEN, keys, help_text
from extensions import ConvertionException, MoneyConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.reply_to(message, f'Добрый день! Я Bot convertor, вот что я умею: \n' + help_text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)