import csv
from typing import List, Dict
from io import StringIO


def generate_csv(records: List[Dict]) -> str:
    if not records:
        raise ValueError("CSV出力対象のデータが空です")

    fieldnames = records[0].keys()
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in records:
        writer.writerow(row)

    return output.getvalue()
