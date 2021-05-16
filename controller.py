import sys, threading
import bank.py
import atm.py

# Key is card number, value is account id
accounts = {"0000": 0, "1111": 1, "2222": 0}
balances = {0: 2000, 1: 1000}
# Key is card number, value is card PIN Number
passwords = {"0000": 1234, "1111": 7888, "2222": 1234}

# Create mutex locks with keys account ids and values corresponding locks. This is to prevent concurrency issues with user
# being able to do operations from different ATMs.
locks = {0: threading.Lock(), 1: threading.Lock()}

def checkCardIntegrity(isValid):
    return isValid

# This function executes after the card is inserted
def main():
    if not checkCardIntegrity(sys.argv[1]):
        raise ValueError("Card is bad")
    cardNumber = sys.argv[2]
    inputPIN = sys.argv[3]
    ATMId = sys.argv[4]
    if (not bank.checkPIN(cardNumber, inputPIN)):
        raise ValueError("Wrong PIN")

    accountId = bank.getAccountId(cardNumber)

    locks[accountId].acquire()

    operation = sys.argv[5]

    if operation == "Balance":
        print(balances[accountId])
    elif operation == "Deposit":
        amount = sys.argv[6]
        if atm.depositCash(ATMId, amount):
            deposit(accountId, amount)
        else:
            locks[accountId].release()
            raise ValueError("Something went wrong")
    elif operation == "Withdrawal":
        amount = sys.argv[6]
        if not enoughBalance(accountId, amount):
            locks[accountId].release()
            raise ValueError("Not enough money in the account balance")
        try atm.withdrawCash(ATMId, amount):
            withdraw(accountId, amount)
        except ValueError(err):
            locks[accountId].release()
            raise ValueError(err)
    
    locks[accountId].release()




# Method for checking correctness of user input PIN
def checkPIN(cardNumber, inputPIN):
    actualPIN = passwords.get(cardNumber)
    return actualPIN == inputPIN

def getAccountId(cardNumber):
    return accounts[cardNumber]
def enoughBalance(accountId, val):
    return balances[accountId] >= val

def deposit(accountId, val):
    balances[accountId] += val

def withdraw(accountId, val):
    balances[accountId] -= val