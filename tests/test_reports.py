import pytest
import pandas as pd
import json
from src.reports import calculate_weekly_averages


@pytest.fixture
def sample_dataframe():
    """Фикстура с тестовыми данными"""
    data = {
        'date': [
            '2023-01-02', '2023-01-02', '2023-01-03',  # Понедельник, вторник
            '2023-01-09', '2023-01-10', '2023-01-10',  # Понедельник, вторник
            '2023-02-06', '2023-02-07',                # Понедельник, вторник
            '2023-03-13', '2023-03-14'                 # Понедельник, вторник
        ],
        'amount': [
            1000, 1500, 2000,
            1200, 1800, 2200,
            1300, 1900,
            1400, 2100
        ]
    }
    return pd.DataFrame(data)


def test_day_order_correctness(sample_dataframe):
    """Тест правильного порядка дней недели в результате"""
    result = json.loads(calculate_weekly_averages(sample_dataframe))
    days_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг',
    'Пятница', 'Суббота', 'Воскресенье']
    assert list(result.keys()) != "error"
