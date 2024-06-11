import pytest
from task6 import BankAccount

# Happy Path
def test_bank_account_constructor():
    account = BankAccount()
    assert account
    assert account._balance == 0
    assert account._transactions == []


@pytest.mark.parametrize("amount,expected_balance,starting_balance", [(100, 900.0, 1000.0)])
def test_withdrawal_with_int(amount: int, expected_balance: float, starting_balance: float):
    account = BankAccount()
    account._balance += starting_balance
    account.withdrawal(amount)
    assert account._balance == expected_balance


@pytest.mark.parametrize("amount,expected_balance,starting_balance", [(100.0, 900.0, 1000.0), (1, 0, 1)])
def test_withdrawal_with_float(amount: float, expected_balance: float, starting_balance: float):
    account = BankAccount()
    account._balance += starting_balance
    account.withdrawal(amount)
    assert account._balance == expected_balance


@pytest.mark.parametrize("amount,expected_balance,starting_balance", [(100.0, 1100.0, 1000.0), (1.0, 2.0, 1.0)])
def test_deposit_with_float(amount: float, expected_balance: float, starting_balance: float):
    account = BankAccount()
    account._balance += starting_balance
    account.deposit(amount)
    assert account._balance == expected_balance


def test_balance():
    account = BankAccount()
    account._balance += 10000
    assert account.check_balance() == 10000


@pytest.mark.parametrize("transfer_amount, starting_balance_acc1, starting_balance_acc2, expected_balance_acc1,"
                         " expected_balance_acc2", [(100.0, 1000.0, 1000.0, 900.0, 1100.0), (1.0, 1.0, 1.0, 0.0, 2.0)])
def test_transfer_with_float(transfer_amount: float, starting_balance_acc1: float, starting_balance_acc2: float,
                             expected_balance_acc1: float, expected_balance_acc2: float):
    account1 = BankAccount()
    account2 = BankAccount()
    account1._balance += starting_balance_acc1
    account2._balance += starting_balance_acc2
    account1.transfer(account2, transfer_amount)
    assert account1._balance == expected_balance_acc1
    assert account2._balance == expected_balance_acc2


@pytest.mark.parametrize("transfer_amount, starting_balance_acc1, starting_balance_acc2, expected_balance_acc1,"
                         " expected_balance_acc2", [(100, 1000.0, 1000.0, 900.0, 1100.0), (1, 1.0, 1.0, 0.0, 2.0)])
def test_transfer_with_int(transfer_amount: int, starting_balance_acc1: float, starting_balance_acc2: float,
                           expected_balance_acc1: float, expected_balance_acc2: float):
    account1 = BankAccount()
    account2 = BankAccount()
    account1._balance += starting_balance_acc1
    account2._balance += starting_balance_acc2
    account1.transfer(account2, transfer_amount)
    assert account1._balance == expected_balance_acc1
    assert account2._balance == expected_balance_acc2


def test_adding_history():
    account1 = BankAccount()
    account2 = BankAccount()
    assert len(account1.history()) == 0
    assert len(account2.history()) == 0
    account1._balance += 1
    account2._balance += 1
    account1.transfer(account2, 1)
    assert len(account1.history()) == 1
    assert len(account2.history()) == 1
    assert account1.history()[0]["from"] == account1
    assert account1.history()[0]["to"] == account2
    assert account1.history()[0]["amount"] == 1
    assert account2.history()[0]["from"] == account1
    assert account2.history()[0]["to"] == account2
    assert account2.history()[0]["amount"] == 1


# Sad Path
@pytest.mark.parametrize("amount", [True, False, "ABCD", "1", (1, 2, 3)])
def test_withdrawal_with_wrong_types(amount):
    with pytest.raises(ValueError) as e_info:
        account = BankAccount()
        account.withdrawal(amount)


@pytest.mark.parametrize("amount", [True, False, "ABCD", "1", (1, 2, 3)])
def test_deposit_with_wrong_types(amount):
    with pytest.raises(ValueError) as e_info:
        account = BankAccount()
        account.deposit(amount)


@pytest.mark.parametrize("amount", [True, False, "ABCD", "1", (1, 2, 3)])
def test_transfer_with_amount_wrong_types(amount):
    with pytest.raises(ValueError) as e_info:
        account1 = BankAccount()
        account2 = BankAccount()
        account1.transfer(account2, amount)


@pytest.mark.parametrize("account", [True, False, "ABCD", "1", (1, 2, 3)])
def test_transfer_with_account_wrong_types(account):
    with pytest.raises(ValueError) as e_info:
        account1 = BankAccount()
        account1.transfer(account, 1)


def test_transfer_with_negative_balance_result():
    with pytest.raises(Exception) as e_info:
        account1 = BankAccount()
        account2 = BankAccount()
        account1.transfer(account2, 1)
        assert e_info.type == BankAccount.SubtractionToNegativeBalanceException


def test_withdrawal_with_negative_balance_result():
    with pytest.raises(Exception) as e_info:
        account1 = BankAccount()
        account1.withdrawal(1)
        assert e_info.type == BankAccount.SubtractionToNegativeBalanceException
