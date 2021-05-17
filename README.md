# Simple-ATM-Controller

The controller uses Python native packages only, so the only requirement is to have Python installed in your environment. Python 3.7+ versions should be able to work. If not, please upgrade it to Python 3.8.0.

After cloning the repository, open your terminal and run "python3 controller.py". 

1. Terminal will ask you to insert your card. You have to type T to proceed further. Any other input will result in "Card is bad" output
2. Then it will ask for card number. You can type either 0000, 1111 or 2222.
3. For PIN number, input corresponding PIN: {0000: 1234, 1111: 7888, 2222: 4321}
4. Then choose operation. You have to type number from 1 to 4 depending on what you want. Options will be shown in the terminal window
5. For depositing and withdrawal, you will be asked to input amount
6. You can exit by typing 4 or pressing Ctrl-C


To run tests, open your terminal window and run "python3 tests.py" command. I used unittest for tests. 

You can see comments on important parts of the code, both in "controller.py" and "tests.py" files. "balances.json" file is used as a storage for balances, feel free to change the values.

As a side note, you can delete lock related lines in deposit() and withdraw() functions in controller.py and run python3 tests.py. It should fail concurrency test.
