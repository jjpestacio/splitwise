from dataclasses import dataclass
from datetime import date

from splitwise import User
from splitwise.expense import ExpenseUser, Expense


@dataclass
class Transaction:
    amount: float
    description: str
    date: date


class SharedExpense(Expense):
    def __init__(
        self,
        *,
        transaction: Transaction,
        group_id: int,
        payer: User,
        contributor: User,
    ):
        super().__init__()

        first_share = round(transaction.amount / 2, ndigits=2)
        second_share = transaction.amount - first_share

        expense_payer = ExpenseUser()
        expense_payer.id = payer.id
        expense_payer.paid_share = transaction.amount
        expense_payer.owed_share = first_share

        expense_contributor = ExpenseUser()
        expense_contributor.id = contributor.id
        expense_contributor.paid_share = 0
        expense_contributor.owed_share = second_share

        self.setGroupId(group_id)
        self.setUsers([expense_payer, expense_contributor])
        self.setDescription(transaction.description)
        self.setDate(transaction.date.isoformat())
        self.setCost(transaction.amount)
        self.setSplitEqually()
