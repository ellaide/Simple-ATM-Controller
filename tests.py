import unittest, time, threading, sys
import controller
from random import randrange


class TestSum(unittest.TestCase):
    # Single transactions
    def deposit_single(self, amount):
        initialBalance = controller.getBalance(0)
        controller.deposit(0, amount)
        finalBalance = controller.getBalance(0)
        self.assertEqual(initialBalance + amount, finalBalance, "Balances do not match")
    
    def withdraw_single(self, amount):
        initialBalance = controller.getBalance(0)
        controller.withdraw(0, amount)
        finalBalance = controller.getBalance(0)
        self.assertEqual(initialBalance - amount, finalBalance)

    # Check if balance is negative. It shouldn't be
    def test_negative_balance(self):
        initialBalance = controller.getBalance(0)
        self.assertGreaterEqual(initialBalance, 0, "Balance can't be negative")
        
    # Check if user can withdraw more than left in the balance
    def test_withdraw_overflow(self):
        initialBalance = controller.getBalance(0)
        controller.withdraw(0, initialBalance + 1)
        finalBalance = controller.getBalance(0)
        self.assertEqual(initialBalance, finalBalance, "Shouldn't be able to withdraw more than left in the balance")

    # Bunch of single transactions
    def test_many_single_ops(self):
        for i in range(100):
            amount = randrange(100)
            self.deposit_single(amount)
            self.withdraw_single(amount)
            self.test_negative_balance()

    # Create lots of threads doing set of transactions which in the end do not change balance
    def concurrent_operations(self):
        def helper():
            controller.deposit(0, 100)
            # Sleep the thread
            time.sleep(0.001)
            controller.withdraw(0, 100)
        # Make thread switching more frequent
        try:
            sys.setswitchinterval(1e-10)
        except AttributeError:
            sys.setcheckinterval(1)
        threads = []
        for i in range(100):
            thread = threading.Thread(target=helper)
            threads.append(thread)
            thread.start()
        
        for i in range(100):
            threads[i].join()

    # This test runs concurrent operations 10 times to make sure that balance before and after are the same
    def test_concurrency(self):
        initialBalance = controller.getBalance(0)
        for _ in range(10):
            self.concurrent_operations()
        finalBalance = controller.getBalance(0)
        self.assertEqual(initialBalance, finalBalance)

if __name__ == '__main__':
    controller.readFromJSON()
    unittest.main()



