import pandas as pd
from datetime import datetime, timedelta
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reports.log'),
        logging.StreamHandler()
    ]
)


def calculate_weekly_averages(df, end_date=None):
    """Рассчитывает средние траты по дням недели за последние 3 месяца
    и возвращает результат в формате JSON"""
    try:
        if end_date is None:
            end_date = datetime.now()
        elif isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        logging.info(f"Расчет для даты окончания: {end_date}")
        start_date = end_date - timedelta(days=90)
        logging.info(f"Дата начала периода: {start_date}")
        df['date'] = pd.to_datetime(df['date'])
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask].copy()
        if filtered_df.empty:
            logging.warning("Нет данных за указанный период")
            return json.dumps({"error": "Нет данных за указанный период"}, ensure_ascii=False)
        days_ru = {
            'Monday': 'Понедельник',
            'Tuesday': 'Вторник',
            'Wednesday': 'Среда',
            'Thursday': 'Четверг',
            'Friday': 'Пятница',
            'Saturday': 'Суббота',
            'Sunday': 'Воскресенье'
        }
        filtered_df['day_of_week'] = filtered_df['date'].dt.day_name().map(days_ru)
        result = filtered_df.groupby('day_of_week')['amount'].mean().round(2).to_dict()
        days_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                      'Пятница', 'Суббота', 'Воскресенье']
        ordered_result = {day: float(result.get(day, 0)) for day in days_order}
        logging.info("Расчет завершен успешно")
        return json.dumps(ordered_result, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Ошибка при расчете средних трат: {e}", exc_info=True)
        return json.dumps({"error": str(e)}, ensure_ascii=False)
