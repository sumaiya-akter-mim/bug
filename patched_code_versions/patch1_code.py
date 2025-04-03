from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Set up tracing (same as original)
provider = TracerProvider()
processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

class BankAccount:
    def __init__(self, account_holder, initial_balance):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transaction_history = []
        
    def deposit(self, amount):
        with tracer.start_as_current_span("deposit"):
            if amount <= 0:
                raise ValueError("Deposit amount must be positive")
            self.balance += amount
            self.transaction_history.append(("deposit", amount))  # Fixed typo
            
    def withdraw(self, amount):
        with tracer.start_as_current_span("withdraw"):
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")
            if amount > self.balance:
                raise ValueError("Insufficient funds")
            self.balance -= amount
            self.transaction_history.append(("withdraw", amount))
            
    def get_balance(self):
        with tracer.start_as_current_span("get_balance"):
            return self.balance
            
    def get_transaction_history(self):
        with tracer.start_as_current_span("get_transaction_history"):
            return self.transaction_history  # Fixed typo
