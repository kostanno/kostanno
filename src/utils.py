
import logging
from datetime import datetime
import pandas as pd
import requests


(logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('utils.log'),]))


def get_greeting(time_str):
    """Возвращает приветствие в зависимости от времени"""
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        hour = dt.hour
        if 5 <= hour < 12:
            greeting = "Доброе утро"
        elif 12 <= hour < 18:
            greeting = "Добрый день"
        elif 18 <= hour < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"
        logging.info(f"Определено приветствие: {greeting} для времени {time_str}")
        return greeting
    except Exception as e:
        logging.error(f"Ошибка в get_greeting: {e}", exc_info=True)
        return "Привет"


def excel_to_json(excel_path):
    """Читает Excel-файл и возвращает JSON-ответ с данными по картам"""
    try:
        logging.info(f"Чтение Excel-файла: {excel_path}")
        df = pd.read_excel(excel_path)
        cards = []
        for _, row in df.iterrows():
            card_number = str(row.get('Номер карты', '')).strip()
            amount = float(row.get('Сумма платежа', 0))
            cashback = str(row.get("Кэшбэк", 0))
            cards.append({
                'Номер карты': card_number,
                'Сумма платежа': amount,
                'Кэшбэк': cashback
            })
        logging.info(f"Успешно обработано {len(cards)} карт")
        return cards
    except Exception as e:
        logging.error(f"Ошибка в excel_to_json: {e}", exc_info=True)
        return []


def get_currency_rates():
    """Получает курсы валют с API"""
    try:
        logging.info("Запрос курсов валют...")
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        rates = {
            'USD': data['rates']['RUB'],
            'EUR': data['rates']['RUB']
        }
        logging.info(f"Получены курсы валют: {rates}")
        return rates
    except Exception as e:
        logging.error(f"Ошибка в get_currency_rates: {e}", exc_info=True)
        return {'USD': 0, 'EUR': 0}


def get_sp500_price():
    """Получает стоимость S&P500."""
    try:
        logging.info("Запрос стоимости S&P500...")
        response = requests.get("https://api.iextrading.com/1.0/stock/market/quote?symbols=SPY")
        response.raise_for_status()
        data = response.json()
        price = data[0]['latestPrice']
        logging.info(f"Получена цена S&P500: {price}")
        return price
    except Exception as e:
        logging.error(f"Ошибка в get_sp500_price: {e}", exc_info=True)
        return 0
