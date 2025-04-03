import unittest
from original_buggy_code.code import BankAccount as Code
from patched_code_versions.patch1_code import BankAccount as Patched1code
from patched_code_versions.patch2_code import BankAccount as Patched2code

class TestBankAccount(unittest.TestCase):
    def test_deposit_and_withdraw(self):
        for account_class in [Code, Patched1code, Patched2code]:
            with self.subTest(account_class=account_class):
                account = account_class("Test User", 100)
                account.deposit(50)
                self.assertEqual(account.get_balance(), 150)
                account.withdraw(30)
                self.assertEqual(account.get_balance(), 120)
                
    def test_transaction_history(self):
        for account_class in [Patched1code, Patched2code]:
            with self.subTest(account_class=account_class):
                account = account_class("Test User", 100)
                account.deposit(50)
                account.withdraw(30)
                history = account.get_transaction_history()
                self.assertEqual(len(history), 2)
                self.assertEqual(history[0], ("deposit", 50))
                self.assertEqual(history[1], ("withdraw", 30))
                
    def test_negative_deposit(self):
        for account_class in [Code, Patched1code, Patched2code]:
            with self.subTest(account_class=account_class):
                account = account_class("Test User", 100)
                with self.assertRaises(ValueError):
                    account.deposit(-10)
                    
    def test_insufficient_funds(self):
        for account_class in [Code, Patched1code, Patched2code]:
            with self.subTest(account_class=account_class):
                account = account_class("Test User", 100)
                with self.assertRaises(ValueError):
                    account.withdraw(150)

if __name__ == "__main__":
    unittest.main()
