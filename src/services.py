import json
import logging
import re


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('services.log'),
        logging.StreamHandler()
    ]
)


def get_person_transfers(transactions):
    """Фильтрует транзакции по переводам физлицам"""
    try:
        logging.info("Начало обработки транзакций")
        pattern = re.compile(r'^[А-ЯЁ][а-яё]+ [А-ЯЁ]\.$')
        person_transfers = []
        for tx in transactions:
            if (tx.get('category') == 'Переводы' and
                    isinstance(tx.get('description'), str) and
                    pattern.match(tx['description'].strip())):
                person_transfers.append({
                    'date': tx.get('date'),
                    'amount': tx.get('amount'),
                    'description': tx.get('description'),
                    'card_last4': tx.get('card')[-4:] if tx.get('card') else None
                })
        logging.info(f"Найдено {len(person_transfers)} переводов физлицам")
        return json.dumps(person_transfers, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Ошибка при фильтрации переводов: {e}", exc_info=True)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
