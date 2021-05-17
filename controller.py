import sys, threading, json


# Key is card number, value is account id. There are cases where two cards are linked to the same account
accounts = {0000: 0, 1111: 1, 2222: 0}

# Key is card number, value is card PIN Number
passwords = {0000: 1234, 1111: 7888, 2222: 4321}

# Create mutex locks with keys as account ids and values as corresponding locks. This is to prevent concurrency issues with user
# being able to do operations from different ATMs and same account
locks = {0: threading.Lock(), 1: threading.Lock()}

# Balances are stored in the JSON file. In reality, this should be database (SQL)
strBalances = json.load(open("balances.json"))
balances = {}

# Trivial implementation to check card validity
def checkCardIntegrity(isValid):
    return isValid

def main():
    # Read from JSON file to balances with correct format
    readFromJSON()
    
    print("Insert your card")
    # For simplicity, Type T as input if card is valid. If you type anything else, checkCardIntegrity will result in False
    validity = input()
    if not checkCardIntegrity(validity == "T"):
        print("Card is bad")
        return

    # In real system, we don't ask this, since ATM card reader will give us this information. Please take a look at the 
    # passwords dict to check card number and PIN correspondence
    print("Input your card number: ", end = '')
    cardNumber = int(input())

    # I didn't hide PIN since I don't think it's essential for this task
    print("Type PIN: ", end = '')
    inputPIN = int(input())
    if not checkPIN(cardNumber, inputPIN):
        print("Wrong PIN")
        return

    # There are cases when two cards are linked to the same account.
    accountId = getAccountId(cardNumber)
    
    print("Choose account: ")
    for account in balances[accountId]:
        print(account, end=" ")
    print("")
    accountType = input()
    found = False
    for account in balances[accountId]:
        if accountType == account:
            found = True
            break
    if not found:
        print("Account name", accountType, "does not exist")
        return
    # This is an infinite loop. It will break when user types 4

    while True:
        print("Choose operation: 1 - Balance, 2 - Deposit, 3 - Withdraw, 4 - Exit")
        operation = int(input())
        if operation == 1:
            print("Current Balance is", getBalance(accountId, accountType))
        elif operation == 2:
            print("Input amount in USD: ", end = '')
            amount = int(input())
            if not deposit(accountId, accountType, amount):
                print("Something went wrong")
                return
            print("Current Balance is", getBalance(accountId, accountType))
        elif operation == 3:
            print("Input amount in USD: ", end = '')
            amount = int(input())
            if not withdraw(accountId, accountType, amount):
                print("Not enough funds")
            else:
                print("Current Balance is", getBalance(accountId, accountType))
        elif operation == 4:
            break


def readFromJSON():
    for key in strBalances:
        accounts = {}
        for acc in strBalances[key]:
            accounts[acc] = int(strBalances[key][acc])
        balances[int(key)] = accounts

# Method for checking correctness of user input PIN
def checkPIN(cardNumber, inputPIN):
    actualPIN = passwords.get(cardNumber)
    return actualPIN == inputPIN

def getAccountId(cardNumber):
    return accounts[cardNumber]
def enoughBalance(accountId, accountType, val):
    return balances[accountId][accountType] >= val

def getBalance(accountId, accountType):
    return balances[accountId][accountType]

# In the deposit() and withdraw() functions, we can integrate with ATM cash bin. For deposit, we need to line which adds money to ATM cash bin
# For withdrawal, we need to first check if there are enough funds in the cash bin, if there are, then check
# if user's balance can be updated successfully. If yes, then give out the cash and decrement ATM cash bin value
def deposit(accountId, accountType, val):
    # Use locks to prevent races. Try commenting our lines with locks and run python3 tests.py. It shouldn't pass concurrency test
    locks[accountId].acquire()    
    balances[accountId][accountType] += val
    # Save the data to persistent storage
    saveToBalances()
    success = True
    locks[accountId].release()
    return success

def withdraw(accountId, accountType, val):
    # Use locks to prevent races
    locks[accountId].acquire()
    success = False
    if (enoughBalance(accountId, accountType, val)):
        balances[accountId][accountType] -= val
        # Save the data to persistent storage
        saveToBalances()
        success = True
    locks[accountId].release()
    return success

def saveToBalances():
    with open("balances.json", 'w') as json_file:
        json.dump(balances, json_file)

if __name__ == "__main__":
    main()