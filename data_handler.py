from collections import namedtuple
from typing import Iterable, Union, Optional
from abc import ABC, abstractmethod

SumResult = namedtuple('SumResult', ['total', 'count', 'incorrect_count'])

class DataHandler(ABC):
    @abstractmethod
    def process_data(self, data: Iterable[float]) -> SumResult:
        """
        Процессирует данные и возвращает результат суммирования.

        Args:
            data (Iterable[float]): Итерируемый объект, содержащий числовые значения.

        Returns:
            SumResult: Результат суммирования.
        """
        pass

    def _process_data(self, data: Iterable[Union[int, float, str]]) -> SumResult:
        total_sum = 0.0
        count = 0
        incorrect_count = 0

        for item in map(self._process_item, data):
            if item is not None:
                total_sum += item
                count += 1
            else:
                incorrect_count += 1

        return SumResult(total=total_sum, count=count, incorrect_count=incorrect_count)

    @abstractmethod
    def _process_item(self, item: Union[int, float, str]) -> Optional[float]:
        """
        Обрабатывает отдельный элемент данных.

        Args:
            item (Union[int, float, str]): Элемент данных, который нужно обработать.

        Returns:
            Optional[float]: Обработанный элемент или None, если элемент некорректен.
        """
        pass

# Пример реализации DataHandler
class SimpleDataHandler(DataHandler):
    def process_data(self, data: Iterable[float]) -> SumResult:
        return self._process_data(data)

    def _process_item(self, item: Union[int, float, str]) -> Optional[float]:
        try:
            # Пробуем преобразовать элемент в float
            return float(item)
        except (ValueError, TypeError):
            # Если не удалось преобразовать, возвращаем None
            return None
