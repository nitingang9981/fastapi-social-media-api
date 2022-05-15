
class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise InsufficientFunds("Insufficient funds")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1