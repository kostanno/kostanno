import logging
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from pandas.io import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()


API_KEY = os.getenv("API_KEY")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("utils.log"),
    ],
)


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


def excel_to_json(excel_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Читает Excel-файл и возвращает JSON-ответ с данными по картам и транзакциям
    """
    try:
        logging.info(f"Чтение Excel-файла: {excel_path}")
        df = pd.read_excel(excel_path)

        # Обработка данных по картам
        cards_data = []
        card_groups = df.groupby("Номер карты")

        for card_number, group in card_groups:
            last_digits = str(card_number)[-4:] if pd.notna(card_number) else "0000"
            total_spent = group["Сумма платежа"].sum()
            cashback = total_spent / 100  # 1% кешбэк

            cards_data.append(
                {
                    "last_digits": last_digits,
                    "total_spent": round(float(total_spent), 2),
                    "cashback": round(float(cashback), 2),
                }
            )
        transactions = []
        if not df.empty:
            top_trans = df.nlargest(5, "Сумма платежа", keep="all")
            for _, row in top_trans.iterrows():
                transactions.append(
                    {
                        "date": row["Дата"].strftime("%d.%m.%Y") if pd.notna(row.get("Дата")) else "01.01.1970",
                        "amount": round(float(row["Сумма платежа"]), 2),
                        "category": str(row.get("Категория", "Не указана")),
                        "description": str(row.get("Описание", "Нет описания")),
                    }
                )
        logging.info(f"Успешно обработано {len(cards_data)} карт и {len(transactions)} транзакций")
        return {"cards": cards_data, "top_transactions": transactions}
    except Exception as e:
        logging.error(f"Ошибка в excel_to_json: {e}", exc_info=True)
        return {"cards": [], "top_transactions": []}


def load_user_settings():
    """Загружает настройки валют и акций из файла"""
    try:
        with open("user_settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}


def get_currency_rates(currencies=["USD", "EUR"]):
    """Получает курсы валют через exchangerates_data API"""
    rates = []
    api_key = "qguILuxpZJZ1TAjPtUWTdl49T0mxG3Sn"
    try:
        symbols = ",".join(currencies)
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base=RUB"
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        for currency in currencies:
            if currency in data.get("rates", {}):
                rate = round(1 / data["rates"][currency], 4)
                rates.append({"currency": currency, "rate": rate})
            else:
                rates.append({"currency": currency, "rate": 0})
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе курсов валют: {e}")
        rates = [{"currency": currency, "rate": 0} for currency in currencies]
    return rates


def get_sp500_price() -> List[Dict[str, float]]:
    """
    Получает текущие цены акций из списка в user_settings.json

    """
    try:
        with open("../data/user_settings.json", "r") as f:
            settings = json.load(f)
            stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        if not stocks:
            logging.warning("В user_settings.json не указаны акции")
            return []
        logging.info(f"Запрос цен для акций: {stocks}")
        API_KEY = "5BK9STW9CU9CIAPY"
        result = []
        for symbol in stocks:
            try:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                if "Global Quote" in data:
                    price = float(data["Global Quote"]["05. price"])
                    result.append({"stock": symbol, "price": round(price, 2)})
                else:
                    logging.warning(f"Не удалось получить цену для {symbol}")
            except Exception as e:
                logging.error(f"Ошибка при получении цены для {symbol}: {e}")
                continue
        logging.info(f"Успешно получены цены для {len(result)} акций")
        return result
    except FileNotFoundError:
        logging.error("Файл user_settings.json не найден")
        return []
