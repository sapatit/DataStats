import json
import logging
from pathlib import Path
from typing import Iterable, Union, Optional
from data_handler import DataHandler, SumResult

logger = logging.getLogger(__name__)

class JSONDataHandler(DataHandler):
    """
    Обработчик данных, считывающий данные из JSON-файла.
    """
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def process_data(self) -> SumResult:
        """
        Обрабатывает данные из JSON-файла и возвращает результат суммирования.

        Returns:
            SumResult: Результат суммирования.
        """
        try:
            with self.file_path.open('r') as f:
                data = json.load(f)
                return self._process_data(data)
        except (IOError, OSError) as e:
            logger.error(f"Ошибка при обработке файла: {e}")
            return SumResult(total=0.0, count=0, incorrect_count=0)

    def _process_item(self, item: Union[int, float, str]) -> Optional[float]:
        try:
            return float(item)
        except (ValueError, TypeError):
            return None
