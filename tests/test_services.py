from unittest.mock import patch
import re
import json
import logging
from src.services import get_person_transfers


def test_empty_transactions():
    """Тест обработки пустого списка транзакций"""
    result = json.loads(get_person_transfers([]))
    assert len(result) == 0


def test_missing_card_number():
    """Тест обработки отсутствующего номера карты"""
    test_transactions = [
        {
            'category': 'Переводы',
            'description': 'Сидоров С.',
            'date': '2023-01-01',
            'amount': 1000,
            'card': None
        }
    ]
    result = json.loads(get_person_transfers(test_transactions))
    assert len(result) == 1
    assert result[0]['card_last4'] is None


@patch('re.compile')
def test_regex_error(mock_compile):
    """Тест обработки ошибки компиляции регулярного выражения"""
    mock_compile.side_effect = re.error("Regex error")
    with patch.object(logging, 'error') as mock_logging:
        result = json.loads(get_person_transfers([]))
        assert isinstance(result, dict)
        assert 'error' in result
        mock_logging.assert_called_once()
