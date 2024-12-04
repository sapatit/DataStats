import unittest
import random
from unittest.mock import patch
from data_processor import DataProcessor, SumResult, AverageResult, process_data


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
        average_result = self.processor.calculate_average()
        self.assertEqual(average_result.average, 15)

    def test_calculate_average_with_no_data(self):
        """Проверяем, что при отсутствии данных возвращается None для среднего и сообщение об ошибке."""
        average_result = self.processor.calculate_average()
        self.assertIsNone(average_result.average)
        self.assertIsNotNone(average_result.error)

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
        """Проверяем, что все некорректные данные обрабатываются правильно."""
        sum_result, average_result = process_data(['abc', 'def', 'ghi'])
        self.assertEqual(sum_result.total, 0.0)
        self.assertEqual(sum_result.count, 0)
        self.assertEqual(sum_result.incorrect_count, 3)
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

    @patch('logging.Logger.warning')
    def test_logging_of_incorrect_data(self, mock_warning):
        process_data([10, 'abc', 20])
        mock_warning.assert_called_with('Некорректные данные: abc - неподдерживаемый тип.')

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


if __name__ == '__main__':
    unittest.main()
