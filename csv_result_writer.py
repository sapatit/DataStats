import csv
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class SumResult:
    total: float
    count: int
    incorrect_count: int

def write_csv_results(file_path: Path, sum_result: SumResult, average_result: Optional[float]) -> None:
    """
    Записывает результаты суммирования и вычисления среднего арифметического в CSV файл.

    Args:
        file_path (Path): Путь к файлу, в который будут записаны результаты.
        sum_result (SumResult): Результат суммирования.
        average_result (Optional[float]): Среднее арифметическое (может быть None, если нет корректных данных).
    """
    results = [
        ["Сумма", sum_result.total],
        ["Некорректные данные", sum_result.incorrect_count],
        ["Среднее арифметическое", average_result if average_result is not None else "Нет данных"]
    ]

    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(results)
        print(f"Результаты записаны в файл: {file_path}")
    except (IOError, OSError) as e:
        print(f"Ошибка при записи в файл: {e}")
