import logging
from pathlib import Path
from json_data_handler import JSONDataHandler
from csv_data_handler import CSVDataHandler
from json_result_writer import write_json_results
from csv_result_writer import write_csv_results
from logger_config import setup_logger

def main():
    setup_logger('logging_config.yaml')
    logger = logging.getLogger(__name__)

    # Путь к файлам данных (можно изменить на нужные вам)
    json_file_path = Path('data.json')  # Замените на ваш JSON файл
    csv_file_path = Path('data.csv')  # Замените на ваш CSV файл
    json_output_file_path = Path('json_results.json')  # Файл для записи результатов в JSON
    csv_output_file_path = Path('csv_results.csv')  # Файл для записи результатов в CSV

    # Обработка данных из JSON
    json_handler = JSONDataHandler(json_file_path)
    sum_result_json = json_handler.process_data()
    average_result_json = sum_result_json.total / sum_result_json.count if sum_result_json.count > 0 else None

    # Обработка данных из CSV
    csv_handler = CSVDataHandler(csv_file_path)
    sum_result_csv = csv_handler.process_data()
    average_result_csv = sum_result_csv.total / sum_result_csv.count if sum_result_csv.count > 0 else None

    # Запись результатов в файл
    write_json_results(json_output_file_path, sum_result_json, average_result_json)
    write_csv_results(csv_output_file_path, sum_result_csv, average_result_csv)

    logging.info(f"Результаты записаны в файлы: {json_output_file_path} и {csv_output_file_path}")

    logger.info("Обработка данных завершена.")

if __name__ == "__main__":
    main()
