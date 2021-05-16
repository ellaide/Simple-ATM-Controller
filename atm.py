import threading
# ATM_id : cash bin amount dictionary
cashAmount = {1: 1000, 2: 2000}

# ATM locks
ATM_locks = {1: threading.Lock(), 2: threading.Lock()}


def withdrawCash(ATM_id, amount):
    ATM_locks[ATM_id].acquire()
    if (cashAmount[ATM_id] < amount):
        ATM_locks[ATM_id].release()
        raise ValueError("Not enough cash left in the ATM")
    cashAmount[ATM_id] -= amount
    ATM_locks[ATM_id].release()
    return True

def depositCash(ATM_id, amount):
    ATM_locks[ATM_id].acquire()
    cashAmount[ATM_id] += amount
    ATM_locks[ATM_id].release()
    return True