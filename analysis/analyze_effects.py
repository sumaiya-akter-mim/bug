from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import sys
import os

# Add the parent directory to the path so we can import the BankAccount class
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from original_buggy_code.code import BankAccount

# Configure OpenTelemetry
resource = Resource(attributes={
    SERVICE_NAME: "bank-account-service"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Create a instrumented version of BankAccount
class InstrumentedBankAccount(BankAccount):
    def deposit(self, amount):
        with tracer.start_as_current_span("deposit_operation") as span:
            span.set_attribute("amount", amount)
            result = super().deposit(amount)
            span.set_attribute("balance_after", self.balance)
            return result

    def withdraw(self, amount):
        with tracer.start_as_current_span("withdraw_operation") as span:
            span.set_attribute("amount", amount)
            span.set_attribute("balance_before", self.balance)
            result = super().withdraw(amount)
            span.set_attribute("balance_after", self.balance)
            span.set_attribute("successful", self.balance != span.get_attribute("balance_before"))
            return result
            
    def display_balance(self):
        with tracer.start_as_current_span("display_balance") as span:
            span.set_attribute("balance", self.balance)
            span.set_attribute("owner", self.owner)
            return super().display_balance()

# Test function to run analysis
def analyze_bank_account():
    with tracer.start_as_current_span("bank_account_test"):
        # Test scenario
        account = InstrumentedBankAccount("Test User", 1000)
        
        # Test operations
        account.deposit(500)
        account.withdraw(200)
        account.withdraw(2000)  # Should fail
        account.deposit(-100)   # Should fail
        account.display_balance()

if __name__ == "__main__":
    analyze_bank_account()
