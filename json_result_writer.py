import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class SumResult:
    total: float
    count: int
    incorrect_count: int

def write_json_results(file_path: Path, sum_result: SumResult, average_result: Optional[float]) -> None:
    """
    Записывает результаты суммирования и вычисления среднего арифметического в JSON файл.

    Args:
        file_path (Path): Путь к файлу, в который будут записаны результаты.
        sum_result (SumResult): Результат суммирования.
        average_result (Optional[float]): Среднее арифметическое (может быть None, если нет корректных данных).
    """
    results = {
        "Сумма": sum_result.total,
        "Некорректные данные": sum_result.incorrect_count,
        "Среднее арифметическое": average_result if average_result is not None else "Нет данных"
    }

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"Результаты записаны в файл: {file_path}")
    except (IOError, OSError) as e:
        print(f"Ошибка при записи в файл: {e}")
