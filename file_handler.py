import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SumResult:
    total: float
    count: int
    incorrect_count: int

def write_results_to_file(file_path: Path, sum_result: SumResult, average_result: Optional[float]) -> None:
    """
    Записывает результаты суммирования и вычисления среднего арифметического в файл.

    Args:
        file_path (Path): Путь к файлу, в который будут записаны результаты.
        sum_result (SumResult): Результат суммирования.
        average_result (Optional[float]): Среднее арифметическое (может быть None, если нет корректных данных).
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Сумма: {sum_result.total}\n")
            f.write(f"Некорректные данные: {sum_result.incorrect_count}\n")
            f.write(f"Среднее арифметическое: {average_result if average_result is not None else 'Нет данных'}\n")
        logger.info(f"Результаты записаны в файл: {file_path}")
    except (IOError, OSError) as e:
        logger.error(f"Ошибка при записи в файл: {e}")
