import threading
import time

class BankAccount:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        current = self.balance
        time.sleep(0.01)  # Simulate operation delay
        self.balance = current + amount
        
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance >= amount:
            current = self.balance
            time.sleep(0.01)  # Simulate operation delay
            self.balance = current - amount
            return True
        return False
        
    def get_balance(self):
        return self.balance