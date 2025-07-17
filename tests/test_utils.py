import pytest
from unittest.mock import patch, MagicMock
from src.utils import excel_to_json, get_greeting, get_currency_rates
from datetime import datetime
import requests


@patch('pandas.read_excel')
def test_excel_to_json(mock_read_excel):
    """Тест успешного чтения Excel-файла и преобразования в JSON"""
    mock_df = MagicMock()
    mock_df.iterrows.return_value = [
        (0, {'Номер карты': '1234 5678 9012 3456', 'Сумма платежа': 1000, 'Кэшбэк': '5%'}),
        (1, {'Номер карты': '1111 2222 3333 4444', 'Сумма платежа': 2000, 'Кэшбэк': '2%'})
    ]
    mock_read_excel.return_value = mock_df
    result = excel_to_json('dummy_path.xlsx')
    assert len(result) == 2
    assert result[0]['Номер карты'] == '1234 5678 9012 3456'
    assert result[0]['Сумма платежа'] == 1000
    assert result[0]['Кэшбэк'] == '5%'
    assert result[1]['Номер карты'] == '1111 2222 3333 4444'


@patch('pandas.read_excel')
def test_excel_to_json1(mock_read_excel):
    """Тест обработки пустого Excel-файла"""
    mock_df = MagicMock()
    mock_df.iterrows.return_value = []
    mock_read_excel.return_value = mock_df
    result = excel_to_json('empty.xlsx')
    assert result == []


@patch('datetime.datetime')
def test_get_greeting(mock_datetime):
    """Тест для утреннего приветствия"""
    mock_datetime.strptime.return_value = datetime(2023, 1, 1, 8, 30, 0)
    assert get_greeting("2023-01-01 08:30:00") == "Доброе утро"


@patch('datetime.datetime')
def test_afternoon_greeting(mock_datetime):
    """Тест для дневного приветствия"""
    mock_datetime.strptime.return_value = datetime(2023, 1, 1, 14, 15, 0)
    assert get_greeting("2023-01-01 14:15:00") == "Добрый день"


@patch('requests.get')
def test_api_error_response(mock_get):
    """Тест обработки ошибки API"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")
    mock_get.return_value = mock_response
    result = get_currency_rates()
    assert result == {'USD': 0, 'EUR': 0}


@patch('requests.get')
def test_connection_error(mock_get):
    """Тест обработки ошибки соединения"""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
    result = get_currency_rates()
    assert result == {'USD': 0, 'EUR': 0}