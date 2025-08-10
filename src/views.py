import json
from utils import excel_to_json, get_greeting, get_currency_rates, get_sp500_price


def main(time_str, excel_path):
    """Главная функция, возвращающая JSON-ответ"""
    greeting = get_greeting(time_str)
    cards = excel_to_json(excel_path)
    currency_rates = get_currency_rates()
    sp500_price = get_sp500_price()
    response = {"greeting": greeting, "cards": cards, "currency_rates": currency_rates, "sp500_price": sp500_price}

    return json.dumps(response, ensure_ascii=False, indent=2)
