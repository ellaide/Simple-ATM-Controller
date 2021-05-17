# Key is card number, value is account id
accounts = {"0000": 0, "1111": 1, "2222": 0}

# Key is card number, value is card PIN Number
passwords = {"0000": 1234, "1111": 7888, "2222": 1234}

# Method for checking correctness of user input PIN
def checkPIN(cardNumber, inputPIN):
    actualPIN = passwords.get(cardNumber)
    return actualPIN == inputPIN

def getAccount(cardNumber):
    return accounts[cardNumber]