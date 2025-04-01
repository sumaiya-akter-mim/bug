from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Setup OpenTelemetry (if running this file directly)
resource = Resource(attributes={
    SERVICE_NAME: "bank-account-patch1"
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
            self.owner = owner
            self.balance = balance
    
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
            
            span.set_attribute("balance_after", self.balance)
            span.set_attribute("success", amount >= 0 and amount <= self.balance)
    
    def display_balance(self):
        with tracer.start_as_current_span("display_balance") as span:
            span.set_attribute("owner", self.owner)
            span.set_attribute("balance", self.balance)
            print(f"Account balance for {self.owner} is: {self.balance}")

# Keep the main code the same as in the original file
if __name__ == "__main__":
    owner = input("Enter account owner's name: ")
    balance = int(input("Enter initial balance: "))
    account = BankAccount(owner, balance)
    
    with tracer.start_as_current_span("main_program"):
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
