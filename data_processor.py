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

    def calculate_average(self) -> AverageResult:
        if self.count == 0:
            return AverageResult(average=None, error="Нет корректных данных для вычисления среднего.")
        average = self.total_sum / self.count
        return AverageResult(average=average, error=None)


def safe_add(processor: DataProcessor, item) -> None:
    if item is None or not isinstance(item, (int, float)):
        logger.warning(f"Некорректные данные: {item} - неподдерживаемый тип.")
        processor.add_incorrect()
        return

    try:
        value = float(item)
        processor.add_value(value)
    except (ValueError, TypeError) as e:
        logger.warning(f"Некорректные данные: {item} - {e}")
        processor.add_incorrect()


def calculate_average(total: float, count: int) -> AverageResult:
    if count == 0:
        return AverageResult(average=None, error="Нет корректных данных для вычисления среднего.")

    average = total / count
    return AverageResult(average=average, error=None)


def handle_data(data: Iterable[float]) -> tuple[SumResult, AverageResult]:
    processor = DataProcessor()
    for item in data:
        safe_add(processor, item)

    sum_result = SumResult(total=processor.total_sum, count=processor.count, incorrect_count=processor.incorrect_count)
    average_result = processor.calculate_average()
    return sum_result, average_result


def process_data(data: Iterable[float]) -> tuple[SumResult, AverageResult]:
    if not data:
        logger.error("Входные данные пусты.")
        return SumResult(total=0.0, count=0, incorrect_count=0), AverageResult(average=None,
                                                                               error="Нет корректных данных для вычисления среднего.")

    return handle_data(data)
