import unittest
import random
import logging
from unittest.mock import patch
from data_processor import DataProcessor, SumResult, AverageResult, process_data
from logger_config import setup_logger


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    def test_add_value(self):
        """Проверяем, что корректное значение добавляется правильно."""
        self.processor.add_value(10)
        self.assertEqual(self.processor.total_sum, 10)
        self.assertEqual(self.processor.count, 1)

    def test_add_incorrect(self):
        """Проверяем, что некорректные данные увеличивают счетчик некорректных значений."""
        self.processor.add_incorrect()
        self.assertEqual(self.processor.incorrect_count, 1)

    def test_calculate_average(self):
        """Проверяем, что среднее значение вычисляется правильно для корректных данных."""
        self.processor.add_value(10)
        self.processor.add_value(20)
        results = self.processor.calculate_results()
        self.assertEqual(results.average, 15)

    def test_calculate_average_with_no_data(self):
        """Проверяем, что при отсутствии данных возвращается None для среднего и сообщение об ошибке."""
        average_result = self.processor.calculate_results()
        self.assertIsNone(average_result.average)
        self.assertEqual(average_result.count, 0)  # Проверяем, что count равен 0
        self.assertEqual(average_result.incorrect_count, 0)  # Проверяем, что incorrect_count равен 0

    def test_process_data_empty(self):
        """Проверяем, что обработка пустых данных возвращает нулевые значения."""
        sum_result, average_result = process_data([])
        self.assertEqual(sum_result.total, 0.0)
        self.assertEqual(sum_result.count, 0)
        self.assertEqual(sum_result.incorrect_count, 0)
        self.assertIsNone(average_result.average)
        self.assertIsNotNone(average_result.error)

    def test_process_data_with_invalid_values(self):
        """Проверяем, что некорректные значения обрабатываются правильно и не влияют на сумму."""
        sum_result, average_result = process_data([10, 'abc', 20])
        self.assertEqual(sum_result.total, 30.0)
        self.assertEqual(sum_result.count, 2)
        self.assertEqual(sum_result.incorrect_count, 1)
        self.assertEqual(average_result.average, 15.0)
        self.assertIsNone(average_result.error)

    def test_process_data_with_all_invalid_values(self):
        sum_result, average_result = process_data(('abc', 'def', 'ghi'))
        self.assertEqual(sum_result.total, 0.0)
        self.assertEqual(sum_result.count, 0)
        self.assertEqual(sum_result.incorrect_count, 3)  # Поскольку все значения некорректные
        self.assertIsNone(average_result.average)
        self.assertIsNotNone(average_result.error)

    def test_process_data_with_mixed_values(self):
        """Проверяем, что смешанные данные обрабатываются правильно."""
        sum_result, average_result = process_data([10, 20, 'abc', 30, 'def'])
        self.assertEqual(sum_result.total, 60.0)
        self.assertEqual(sum_result.count, 3)
        self.assertEqual(sum_result.incorrect_count, 2)
        self.assertEqual(average_result.average, 20.0)
        self.assertIsNone(average_result.error)

    def test_process_data_with_zero_values(self):
        """Проверяем, что нулевые значения обрабатываются корректно."""
        sum_result, average_result = process_data([0, 0, 0])
        self.assertEqual(sum_result.total, 0.0)
        self.assertEqual(sum_result.count, 3)
        self.assertEqual(sum_result.incorrect_count, 0)
        self.assertEqual(average_result.average, 0.0)
        self.assertIsNone(average_result.error)


    def test_process_data_with_injection_attempt(self):
        data = [10, 'abc"; DROP TABLE users; --', 20]
        sum_result, average_result = process_data(data)
        self.assertEqual(sum_result.total, 30.0)
        self.assertEqual(sum_result.count, 2)
        self.assertEqual(sum_result.incorrect_count, 1)
        self.assertEqual(average_result.average, 15.0)

    def test_process_data_with_unsupported_type(self):
        """Проверяем, что при передаче неподдерживаемого типа данных некорректные данные обрабатываются."""
        sum_result, average_result = process_data([10, None, 20])
        self.assertEqual(sum_result.total, 30.0)
        self.assertEqual(sum_result.count, 2)
        self.assertEqual(sum_result.incorrect_count, 1)
        self.assertEqual(average_result.average, 15.0)
        self.assertIsNone(average_result.error)

    def test_docstrings_accuracy(self):
        self.assertIn('Проверяем, что корректное значение добавляется правильно.', self.test_add_value.__doc__)
        self.assertIn('Проверяем, что среднее значение вычисляется правильно для корректных данных.',
                      self.test_calculate_average.__doc__)

    def test_process_random_data(self):
        data = [random.uniform(-100, 100) for _ in range(1000)]
        sum_result, average_result = process_data(data)
        self.assertIsNotNone(sum_result)
        self.assertIsNotNone(average_result)

    def test_process_large_dataset(self):
        data = [i for i in range(10000)]
        sum_result, average_result = process_data(data)
        self.assertIsNotNone(sum_result)
        self.assertIsNotNone(average_result)

    def test_add_negative_value(self):
        self.processor.add_value(-10)
        self.assertEqual(self.processor.total_sum, -10)
        self.assertEqual(self.processor.count, 1)

    def test_add_float_value(self):
        self.processor.add_value(3.14)
        self.assertAlmostEqual(self.processor.total_sum, 3.14)
        self.assertEqual(self.processor.count, 1)

class TestLogging(unittest.TestCase):
    @patch('logging.Logger.info')
    def test_logging_info_message(self, mock_info):
        setup_logger('logging_config.yaml')
        logger = logging.getLogger(__name__)
        logger.info("Тестовое сообщение")

        mock_info.assert_called_with("Тестовое сообщение")

    @patch('logging.Logger.warning')
    def test_logging_warning_message(self, mock_warning):
        setup_logger('logging_config.yaml')
        logger = logging.getLogger(__name__)
        logger.warning("Это предупреждение")

        mock_warning.assert_called_with("Это предупреждение")


if __name__ == '__main__':
    unittest.main()
