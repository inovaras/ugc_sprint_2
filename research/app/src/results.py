from datetime import datetime
from typing import Dict, Any


def save_results_to_file(results: Dict[str, Any]) -> None:
    """
    Сохранение результатов исследования в файл Markdown
    """
    storage_type = results["storage"]
    insert = results["insert"]
    read = results["read"]

    if isinstance(read, tuple):
        read = read[0]

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("results.md", "a") as f:
        f.write(f"## Результаты тестирования {storage_type.upper()} ({current_time})\n\n")

        # Вставка данных
        f.write("#### Время вставки записей в секундах:\n\n")
        f.write(f"- **{insert['total_records']} записей (batch={insert['batch_size']})**: {insert['total_time']:.6f}\n")
        f.write(f"- Среднее время вставки одной записи: {insert['avg_time_per_record']:.6f}\n\n")

        # Чтение данных
        f.write("#### Время чтения записей в секундах:\n\n")
        for table, details in read.items():
            f.write(f"- **{details['count']} записей ({table})**: {details['time']:.6f}\n")
        f.write("\n")
        f.write("____________________________________________________________________________\n\n")
