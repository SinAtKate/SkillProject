import telebot
from utils import CryptoConvert, APIException
from config import currency, TOKEN, sample

bot = telebot.TeleBot(TOKEN)

#обработчик команд /start, /help       
@bot.message_handler(commands=['start', 'help'])
def request_main(message: telebot.types.Message):
    text = sample + '\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)  #вывод ответа пользователю
    
#обработчик команды /values  
@bot.message_handler(commands=['values', ])
def access_currency(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for k in currency.keys():
        text += '\n' + k
    bot.reply_to(message, text)  #вывод ответа пользователю

#обработчик команды на отправку сообщения пользователем
@bot.message_handler(content_types=['text', ])
def convert_currency(message: telebot.types.Message):
    try:
        if len(message.text.split()) != 3:  #сообщение должно содержать 3 слова
            raise APIException(f'Введите запрос по шаблону:\n{sample}')
        
        fsym, tsym, quantity = message.text.split()  #разбиваем текст
        totalConvert = CryptoConvert.get_price(fsym.lower(), tsym.lower(), quantity)  #вызываем статический метод  
    
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        bot.reply_to(message, f'{totalConvert}')  #вывод ответа пользователю
        
bot.polling(none_stop=True)
