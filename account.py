from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

class Account:
    def __init__(
        self,
        accountNumber: str,
        name: str,
        passwordHash: str,
        salt: str,
        address: str | None = None,
        creationDate: datetime | None = None,
        balance: Decimal = Decimal("0.00"),
        transactions: list[dict] | None = None
    ) -> None:
        self.accountNumber = accountNumber
        self.name = name
        self.passwordHash = passwordHash
        self.salt = salt
        self.address = address
        self.creationDate = creationDate
        self.balance = Decimal(str(balance))
        self.transactions = list(transactions) if transactions else []

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount

        now = datetime.now(timezone.utc).isoformat()
        self.transactions.append({
            "type": "deposit",
            "amount": str(amount),
            "date": now
        })

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount

        now = datetime.now(timezone.utc).isoformat()
        self.transactions.append({
            "type": "withdrawal",
            "amount": str(amount),
            "date": now
        })

    def transfer(self, transfereeAccount, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient Funds")

        self.balance -= amount
        transfereeAccount.balance += amount

        now = datetime.now(timezone.utc).isoformat()

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
