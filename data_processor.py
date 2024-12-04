import logging
from typing import Iterable, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AverageResult:
    average: Optional[float]
    error: Optional[str]


@dataclass
class SumResult:
    total: float
    count: int
    incorrect_count: int
    average: Optional[float]


class DataProcessor:
    def __init__(self) -> None:
        self.total_sum: float = 0.0
        self.count: int = 0
        self.incorrect_count: int = 0

    def add_value(self, value: float) -> None:
        self.total_sum += value
        self.count += 1

    def add_incorrect(self) -> None:
        self.incorrect_count += 1

    def calculate_results(self) -> SumResult:
        average = self.total_sum / self.count if self.count > 0 else None
        return SumResult(total=self.total_sum, count=self.count, incorrect_count=self.incorrect_count, average=average)


def safe_add(processor: DataProcessor, item) -> None:
    if item is None or not isinstance(item, (int, float)):
        logger.error(f"Некорректные данные: {item} - неподдерживаемый тип.")
        processor.add_incorrect()
        return

    try:
        value = float(item)
        processor.add_value(value)
    except (ValueError, TypeError) as e:
        logger.error(f"Некорректные данные: {item} - {e}")
        processor.add_incorrect()


def process_data(data: Iterable[float]) -> (SumResult, AverageResult):
    if not data:
        logger.error("Входные данные пусты.")
        sum_result = SumResult(total=0.0, count=0, incorrect_count=0, average=None)
        average_result = AverageResult(average=None, error="Нет данных для расчета среднего.")
        return sum_result, average_result

    processor = DataProcessor()
    for item in data:
        safe_add(processor, item)

    sum_result = processor.calculate_results()
    average_result = AverageResult(average=sum_result.average, error=None)

    if sum_result.count == 0:
        average_result = AverageResult(average=None, error="Нет данных для расчета среднего.")

    return sum_result, average_result
