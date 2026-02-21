from account import Account
import random
import os
import json
import datetime
from decimal import Decimal, InvalidOperation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_FILE = os.path.join(BASE_DIR, "accounts.json")

def generateAccountNumber(length=9):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def getPositiveAmount(prompt):
    while True:
        userInput = input(prompt)
        if userInput.lower() == "cancel":
            return None
        try:
            amount = Decimal(userInput)
            if amount > 0:
                return amount
            print("Amount must be greater than 0")
        except (ValueError, InvalidOperation):
            print("Please enter a valid number")
        
def getValidAccountNumber(prompt="Enter Account Number or type 'cancel': "):
    while True:
        userInput = input(prompt)
        if userInput.lower() == "cancel":
            return None
        lookedUpAccount = accounts.get(userInput)
        if lookedUpAccount:
            return userInput
        print("Account not found. Please try again or type 'cancel'.")

def confirmAction(prompt):
    userInput = input(prompt)
    if userInput.lower() == 'y':
        return True
    else:
        return False

def loadAccounts(filename=ACCOUNTS_FILE):
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}

    with open(filename, "r") as f:
        data = json.load(f)
        accounts = {}
        for k, v in data.items():
            v["creationDate"] = datetime.datetime.fromisoformat(v["creationDate"])
            v["balance"] = Decimal(v["balance"])
            accounts[k] = Account(**v)
        return accounts

def saveAccounts(accounts, filename=ACCOUNTS_FILE):
    with open(filename, "w") as f:
        json.dump(
            {
                k: {
                    **v.__dict__,
                    "balance": str(v.balance),
                    "creationDate": v.creationDate.isoformat()
                }
                for k, v in accounts.items()
            },
            f,
            indent=4
        )

accounts = loadAccounts()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    userInput = input("[1] Open Account\n[2] Enter Account\n[3] Quit\n> ")
    match userInput:
        case "1":
            while True:
                accountNumber = generateAccountNumber()
                if accountNumber not in accounts:
                    break
            name = input("Enter Account Holder Name: ")
            address = input("Enter Account Holder Address: ")
            deposit = getPositiveAmount("Enter Initial Deposit Amount: $")

            accounts[accountNumber] = Account(accountNumber, name, address, datetime.datetime.now(), deposit)
            saveAccounts(accounts)
            print(f"Account #{accountNumber} Created")
            input("Press any key to continue...")
        case "2":
            accountNumber = getValidAccountNumber()
            if accountNumber is None:
                continue
            lookedUpAccount = accounts.get(accountNumber)
            
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"#[{accountNumber}] - {lookedUpAccount.name} - ${lookedUpAccount.balance:,.2f}")
                userInput = input("[1] Deposit Funds\n[2] Withdraw Funds\n[3] Transfer Funds\n[4] Close Account\n[5] Exit Account\n> ")
                match userInput:
                    case "1":
                        amount = getPositiveAmount("Enter Deposit Amount: $")
                        if amount is not None:
                            try:
                                if lookedUpAccount.deposit(amount):
                                    saveAccounts(accounts)
                                    print(f"Deposited ${amount} to [Account #{accountNumber} - {lookedUpAccount.name}]")
                                    input("Press any key to continue...")
                            except ValueError as e:
                                print(f"[ERROR] {e}")
                                input("Press any key to continue...")
                    case "2":
                        amount = getPositiveAmount("Enter Withdrawal Amount: $")
                        if amount is not None:
                            try:
                                if lookedUpAccount.withdraw(amount):
                                    saveAccounts(accounts)
                                    print(f"Withdrew ${amount} from [Account #{accountNumber} - {lookedUpAccount.name}]")
                                    input("Press any key to continue...")
                            except ValueError as e:
                                print(f"[ERROR] {e}")
                                input("Press any key to continue...")
                    case "3":
                        transfereeAccountNumber = getValidAccountNumber("Enter Account Number of Transferee or type 'cancel': ")
                        if transfereeAccountNumber is None:
                            continue
                        transfereeAccount = accounts.get(transfereeAccountNumber)

                        amount = getPositiveAmount(f"Enter amount to transfer to [Account #{transfereeAccount.accountNumber} - {transfereeAccount.name}]: $")

                        if not confirmAction(f"Are you sure you want to transfer ${amount:,.2f} [#{accountNumber} - {lookedUpAccount.name}] --> [#{transfereeAccount.accountNumber} - {transfereeAccount.name}] (Y/N)? "):
                            continue

                        if amount is not None:
                            if lookedUpAccount.transfer(transfereeAccount, amount):
                                saveAccounts(accounts)
                                print(f"Transferred ${amount:,.2f} [#{accountNumber} - {lookedUpAccount.name}] --> [#{transfereeAccount.accountNumber} - {transfereeAccount.name}]")
                                input("Press any key to continue...")
                            else:
                                input(f"Transfer of ${amount:,.2f} failed. Please check your balance and try again.")
                    case "4":
                        if not confirmAction("Are you sure you want to close your account (Y/N)? "):
                            continue
                        
                        print(f"Account #{accountNumber} closing with a balance of ${lookedUpAccount.balance:,.2f} being withdrawn")
                        
                        try:
                            if lookedUpAccount.withdraw(lookedUpAccount.balance):
                                saveAccounts(accounts)
                                print(f"Withdrew ${lookedUpAccount.balance:,.2f} from [Account #{accountNumber} - {lookedUpAccount.name}]")
                                input("Press any key to continue...")
                        except ValueError as e:
                            print(f"[ERROR] {e}")
                            input("Press any key to continue...")
                            continue

                        del accounts[accountNumber]
                        saveAccounts(accounts)

                        input("Press any key to continue...")
                        break
                    case "5":
                        break
        case "3":
            saveAccounts(accounts)
            break