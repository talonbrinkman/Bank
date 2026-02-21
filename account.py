import datetime
from decimal import Decimal, InvalidOperation

class Account:
    def __init__(self, accountNumber, name, address, creationDate, balance=Decimal("0.00"), transactions=None):
        self.accountNumber = accountNumber
        self.name = name
        self.address = address
        self.creationDate = creationDate
        self.balance = Decimal("0.00")
        self.transactions = transactions if transactions is not None else []

        balance = Decimal(str(balance))
        if balance > 0 and self.balance == 0:
            self.deposit(balance)
        else:
            self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount

        now = datetime.datetime.now().isoformat()
        self.transactions.append({
            "type": "deposit",
            "amount": str(amount),
            "date": now
        })

        return True

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount

        now = datetime.datetime.now().isoformat()
        self.transactions.append({
            "type": "withdrawal",
            "amount": str(amount),
            "date": now
        })

        return True

    def transfer(self, transfereeAccount, amount):
        if amount <= 0:
            print("[ERROR] Transfer amount must be positive")
            return False
        if amount > self.balance:
            print("[ERROR] Insufficient funds")
            return False

        self.balance -= amount
        transfereeAccount.balance += amount

        now = datetime.datetime.now().isoformat()

        self.transactions.append({
            "type": "transferSend",
            "amount": str(amount),
            "to": transfereeAccount.accountNumber,
            "date": now
        })

        transfereeAccount.transactions.append({
            "type": "transferReceive",
            "amount": str(amount),
            "from": self.accountNumber,
            "date": now
        })

        return True
