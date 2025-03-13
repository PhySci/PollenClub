import csv
import logging

_logger = logging.getLogger(__name__)


def save_to_csv(data: list, file_path: str) -> None:
    """
    Save comments to csv dataset.

    :param data:
    :param column_names:
    :param file_path:
    :return:
    """
    column_names = data[0].keys()
    with open(file_path, "w", encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_names, delimiter=';')
        try:
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        except Exception as e:
            _logger.error(f"Can't save data to {file_path}", e)
