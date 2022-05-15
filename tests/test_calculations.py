from app.calculations import BankAccount,InsufficientFunds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_bank_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 0

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize("deposited,withdrew,expected",[ (200,100,100)
])
def test_transaction_system(zero_bank_account,deposited,withdrew,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == 100

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(100)
