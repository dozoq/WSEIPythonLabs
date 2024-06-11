import functools
import inspect
import logging
from typing import Self, Callable

logger = logging.getLogger("Xml Parser")
logging.basicConfig(level=logging.DEBUG)


def input_parameters_logging_wrapper(func: Callable) -> Callable:
    # noinspection DuplicatedCode
    @functools.wraps(func)
    def internalFunction(*args, **kwargs):
        parsed_args: str = "{" + f'{func.__qualname__} Operation Called, Args: '
        for ind, (arg, name) in enumerate(zip(args, inspect.signature(func).parameters.values())):
            parsed_args += f"{name}:{type(arg)}={arg}{',' if ind != len(args) - 1 else ''}"
        parsed_args += '}'
        logger.debug(parsed_args)
        result = func(*args, **kwargs)
        return result

    return internalFunction


class BankAccount:
    class SubtractionToNegativeBalanceException(Exception):

        def __init__(self, balance, amount, message="Trying to subtract {amount:.2f} from account {_balance:.2f} "
                                                    "leading to negative _balance {balance_minus_amount:.2f}"):
            self.message = message.format(amount=amount, balance=balance, balance_minus_amount=balance - amount)
            self.balance = balance
            self.amount = amount
            super().__init__(self.message)

    def __init__(self):
        self._balance = 0
        self._transactions = []

    @input_parameters_logging_wrapper
    def withdrawal(self, amount: float) -> float:
        if type(amount) not in [float, int]:
            raise ValueError("Amount must be float/int")
        if self._balance - amount < 0:
            raise self.SubtractionToNegativeBalanceException(self._balance, amount)
        self._balance -= amount

    @input_parameters_logging_wrapper
    def deposit(self, amount: float) -> float:
        if type(amount) not in [float, int]:
            raise ValueError("Amount must be float/int")
        self._balance += amount

    @input_parameters_logging_wrapper
    def check_balance(self) -> float:
        return self._balance

    @input_parameters_logging_wrapper
    def transfer(self, account: Self, amount: float) -> float:
        if type(amount) not in [float, int]:
            raise ValueError("Amount must be float/int")
        if type(account) != BankAccount:
            raise ValueError("Provided account is wrong type")
        if self._balance - amount < 0:
            raise self.SubtractionToNegativeBalanceException(self._balance, amount)
        self.withdrawal(amount)
        account.deposit(amount)
        self._transactions.append({"from": self, "to": account, "amount": amount})
        account._transactions.append({"from": self, "to": account, "amount": amount})
        return self._balance

    @input_parameters_logging_wrapper
    def history(self) -> list:
        return self._transactions

    def __iter__(self):
        return iter(self._transactions)

    def __next__(self):
        return next(self._transactions)

    def __getitem__(self, item):
        return self._transactions[item]


def main():
    account1 = BankAccount()
    account2 = BankAccount()
    account1.deposit(1000)
    account1.transfer(account2, 500)
    account2.withdrawal(250)
    print(account1[0])


if __name__ == '__main__':
    main()
