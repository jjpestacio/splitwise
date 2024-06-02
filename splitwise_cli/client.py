from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import User
import typer

from .constants import JJ_ID, ZOE_ID, GROUP_ID
from .models import SharedExpense, Transaction


class SplitwiseClient:
    def __init__(self, *, consumer_key: str, consumer_secret: str, api_key: str):
        self.client = Splitwise(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            api_key=api_key,
        )

    def get_current_user(self) -> User:
        return self.client.getCurrentUser()

    def get_other_user(self) -> User:
        if self.get_current_user().id == JJ_ID:
            return self.get_friend(user_id=ZOE_ID)

        elif self.get_current_user().id == ZOE_ID:
            return self.get_friend(user_id=JJ_ID)

        raise ValueError("Current user is not JJ or Zoe.")

    def get_friend(self, *, user_id: int) -> User:
        return next(
            friend for friend in self.client.getFriends() if friend.id == user_id
        )

    def add_shared_expense(
        self,
        *,
        transaction: Transaction,
        group_id: int = GROUP_ID,
    ) -> Expense:
        pending_expense = SharedExpense(
            transaction=transaction,
            group_id=group_id,
            payer=self.get_current_user(),
            contributor=self.get_other_user(),
        )

        expense, errors = self.client.createExpense(pending_expense)

        if errors:
            typer.echo(errors.getErrors())
            raise typer.Exit(code=1)

        return expense
