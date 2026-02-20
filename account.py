import datetime

class Account:
    def __init__(self, accountNumber, name, address, creationDate, balance=0, transactions=None):
        self.accountNumber = accountNumber
        self.name = name
        self.address = address
        self.creationDate = creationDate
        self.balance = 0
        self.transactions = []
        self.deposit(balance)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount

        now = datetime.datetime.now().isoformat()
        self.transactions.append({
            "type": "deposit",
            "amount": amount,
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
            "amount": amount,
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
            "amount": amount,
            "to": transfereeAccount.accountNumber,
            "date": now
        })

        transfereeAccount.transactions.append({
            "type": "transferReceive",
            "amount": amount,
            "from": self.accountNumber,
            "date": now
        })

        return True
