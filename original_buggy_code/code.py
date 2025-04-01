class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount < 0:
            print("Cannot deposit a negative amount.")
        else:
            self.balance += amount
            print(f"{amount} deposited successfully!")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        elif amount < 0:
            print("Cannot withdraw a negative amount.")
        else:
            self.balance -= amount
            print(f"{amount} withdrawn successfully!")

    def display_balance(self):
        print(f"Account balance for {self.owner} is: {self.balance}")

# Main code
owner = input("Enter account owner's name: ")
balance = int(input("Enter initial balance: "))
account = BankAccount(owner, balance)

while True:
    print("\n1. Deposit\n2. Withdraw\n3. Show Balance\n4. Exit")
    choice = int(input("Choose an option: "))
    
    if choice == 1:
        amount = int(input("Enter amount to deposit: "))
        account.deposit(amount)
    elif choice == 2:
        amount = int(input("Enter amount to withdraw: "))
        account.withdraw(amount)
    elif choice == 3:
        account.display_balance()
    elif choice == 4:
        print("Exiting...")
        break
    else:
        print("Invalid choice. Try again.")
