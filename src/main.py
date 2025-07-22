from src.reports import calculate_weekly_averages
from src.services import get_person_transfers
from src.views import main


# if __name__ == "__main__":
#     main()
#     get_person_transfers()
#     calculate_weekly_averages()


def run_all_features():
    """Запускает все реализованные функциональности проекта"""
    result1 = calculate_weekly_averages()
    print(result1)
    result2 = get_person_transfers()
    print(result2)
    result3 = main()
    print(result3)


if __name__ == "__main__":
    run_all_features()
