from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Setup OpenTelemetry (if running this file directly)
resource = Resource(attributes={
    SERVICE_NAME: "bank-account-patch2"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

class BankAccount:
    def __init__(self, owner, balance=0):
        with tracer.start_as_current_span("initialize_account") as span:
            span.set_attribute("owner", owner)
            span.set_attribute("initial_balance", balance)
            
            # Validate initial balance
            if balance < 0:
                span.set_attribute("warning", "negative_initial_balance")
                self.balance = 0
                print("Warning: Initial balance cannot be negative. Setting to 0.")
            else:
                self.balance = balance
            
            self.owner = owner
            span.set_attribute("actual_initial_balance", self.balance)
    
    def deposit(self, amount):
        with tracer.start_as_current_span("deposit") as span:
            span.set_attribute("amount", amount)
            span.set_attribute("balance_before", self.balance)
            
            if amount < 0:
                span.set_attribute("error", "negative_amount")
                print("Cannot deposit a negative amount.")
            else:
                self.balance += amount
                print(f"{amount} deposited successfully!")
            
            span.set_attribute("balance_after", self.balance)
            span.set_attribute("success", amount >= 0)
    
    def withdraw(self, amount):
        with tracer.start_as_current_span("withdraw") as span:
            span.set_attribute("amount", amount)
            span.set_attribute("balance_before", self.balance)
            
            if amount > self.balance:
                span.set_attribute("error", "insufficient_funds")
                print("Insufficient funds.")
            elif amount < 0:
                span.set_attribute("error", "negative_amount")
                print("Cannot withdraw a negative amount.")
            else:
                self.balance -= amount
                print(f"{amount} withdrawn successfully!")
                
                # Add a low balance warning
                if self.balance < 100:
                    span.set_attribute("warning", "low_balance")
                    print("Warning: Your balance is below 100.")
            
            span.set_attribute("balance_after", self.balance)
            span.set_attribute("success", amount >= 0 and amount <= self.balance)
    
    def display_balance(self):
        with tracer.start_as_current_span("display_balance") as span:
            span.set_attribute("owner", self.owner)
            span.set_attribute("balance", self.balance)
            print(f"Account balance for {self.owner} is: {self.balance}")

# Enhanced main program with try-except for error handling
if __name__ == "__main__":
    with tracer.start_as_current_span("main_program"):
        try:
            owner = input("Enter account owner's name: ")
            balance_input = input("Enter initial balance: ")
            balance = int(balance_input)
            account = BankAccount(owner, balance)
            
            while True:
                print("\n1. Deposit\n2. Withdraw\n3. Show Balance\n4. Exit")
                choice_input = input("Choose an option: ")
                choice = int(choice_input)
                
                if choice == 1:
                    amount_input = input("Enter amount to deposit: ")
                    amount = int(amount_input)
                    account.deposit(amount)
                elif choice == 2:
                    amount_input = input("Enter amount to withdraw: ")
                    amount = int(amount_input)
                    account.withdraw(amount)
                elif choice == 3:
                    account.display_balance()
                elif choice == 4:
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Try again.")
        except ValueError as e:
            print(f"Error: Invalid input. Please enter numeric values for amounts and choices.")
        except Exception as e:
            print(f"Unexpected error: {e}")
