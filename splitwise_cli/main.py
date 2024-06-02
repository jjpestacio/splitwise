from typing import Annotated

import typer


from .client import SplitwiseClient
from .parsers import CsvFormat, parse_csv

cli = typer.Typer()


@cli.callback()
def commands():
    """Splitwise commands."""


@cli.command()
def add_shared_expenses(
    csv_path: Annotated[
        str,
        typer.Argument(help="The path to the CSV file with transactions."),
    ],
    splitwise_consumer_key: Annotated[
        str,
        typer.Option(prompt=True, help="The consumer key of the Splitwise app."),
    ],
    splitwise_consumer_secret: Annotated[
        str,
        typer.Option(prompt=True, help="The consumer secret of the Splitwise app."),
    ],
    splitwise_api_key: Annotated[
        str,
        typer.Option(prompt=True, help="The API key of the Splitwise app."),
    ],
    csv_format: Annotated[
        CsvFormat,
        typer.Option(help="The transactions format of the CSV file."),
    ] = CsvFormat.CHASE_BANK,
    auto: Annotated[
        bool,
        typer.Option(help="Whether to automatically add all transactions."),
    ] = False,
):
    client = SplitwiseClient(
        consumer_key=splitwise_consumer_key,
        consumer_secret=splitwise_consumer_secret,
        api_key=splitwise_api_key,
    )

    transactions = parse_csv(path=csv_path, format=csv_format)

    for transaction in transactions:
        if auto or typer.confirm(
            f"Would you like to add this transaction: {transaction}?"
        ):
            typer.echo(f"Adding shared expense: {transaction}")
            client.add_shared_expense(transaction=transaction)
