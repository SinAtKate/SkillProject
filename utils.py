import requests
import json
from config import currency

#Класс исключений
class APIException(Exception):
    pass

#Класс конвертирования валют
class CryptoConvert:
    @staticmethod
    def get_price(base, quote, amount):  #статический метод
        try:
            if base not in currency.keys() or quote not in currency.keys():  #проверка на наличие валюты в доступном списке
                raise APIException('Ввели валюту которая не предусмотрена для конвертации')
        
            amount = float(amount)  #преобразование в число
        
        except ValueError:
            raise APIException(f'Невозможно обработать количество: {amount}.\n Ввод числа: 0 или 0.00')

        if base == quote:  #если валюты однотипны
            raise APIException('Укажите валюту различную друг от друга')
        #используем сокращенное обозначение валюты для API из словаря        
        fsym = currency[base]
        tsym = currency[quote]
        #отправляем запрос
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={fsym}&tsyms={tsym}')
        #преобразуем ответ в json словарь
        total_base = json.loads(r.content)
        #обрабатываем полученный словарь
        for key, val in total_base.items(): #разбираем на ключ, значение
            text = key +': '+ str(float('{:.3f}'.format(val*amount)))  #получим сокращенное имя валюты + числовое значение
                                                                        #помноженное на требуемое количество в формате до 3х цифр после запятой 
        return text  #возвращаем готовую строку для вывода пользователю
