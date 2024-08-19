from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import User
from functools import cached_property
import typer

from .users import UserId, GroupId
from .models import SharedExpense, Transaction


class SplitwiseClient:
    def __init__(self, *, consumer_key: str, consumer_secret: str, api_key: str):
        self.client = Splitwise(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            api_key=api_key,
        )

    @cached_property
    def current_user(self) -> User:
        return self.client.getCurrentUser()

    def get_friend(self, *, user_id: UserId) -> User:
        if user_id == self.current_user.id:
            return self.current_user

        return next(
            friend for friend in self.client.getFriends() if friend.id == user_id
        )

    def add_shared_expense(
        self,
        *,
        transaction: Transaction,
        payer_id: UserId,
        contributor_id: UserId,
        group_id: GroupId = GroupId.JJ_AND_ZOE,
    ) -> Expense:
        pending_expense = SharedExpense(
            transaction=transaction,
            group_id=group_id,
            payer=self.get_friend(user_id=payer_id),
            contributor=self.get_friend(user_id=contributor_id),
        )

        expense, errors = self.client.createExpense(pending_expense)

        if errors:
            typer.echo(errors.getErrors())
            raise typer.Exit(code=1)

        return expense
