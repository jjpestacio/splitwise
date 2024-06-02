from datetime import datetime
from enum import Enum
import csv

from .models import Transaction


class CsvFormat(str, Enum):
    CHASE_BANK = "Chase Bank"


def parse_chase_csv(*, path: str) -> list[Transaction]:
    transactions: list[Transaction] = []

    with open(path, newline="") as csvfile:
        transactions = [
            Transaction(
                amount=-float(row["Amount"]),
                date=datetime.strptime(row["Transaction Date"], "%m/%d/%Y").date(),
                description=row["Description"],
            )
            for row in csv.DictReader(csvfile)
        ]

    return transactions


def parse_csv(*, path: str, format: CsvFormat) -> list[Transaction]:
    match format:
        case CsvFormat.CHASE_BANK:
            return parse_chase_csv(path=path)

        case _:
            raise NotImplementedError(f"Format {format} is not supported.")
