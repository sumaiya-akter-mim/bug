import unittest
import sys
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace.status import Status, StatusCode
from io import StringIO
from unittest.mock import patch

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from original_buggy_code.code import BankAccount

# Configure OpenTelemetry
resource = Resource(attributes={
    SERVICE_NAME: "bank-account-tests"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

class TestBankAccount(unittest.TestCase):
    
    def setUp(self):
        with tracer.start_as_current_span("setup_test"):
            self.account = BankAccount("Test User", 1000)
    
    def test_initialization(self):
        with tracer.start_as_current_span("test_initialization") as span:
            span.set_attribute("owner", self.account.owner)
            span.set_attribute("initial_balance", self.account.balance)
            
            self.assertEqual(self.account.owner, "Test User")
            self.assertEqual(self.account.balance, 1000)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_deposit_positive(self, mock_stdout):
        with tracer.start_as_current_span("test_deposit_positive") as span:
            initial_balance = self.account.balance
            span.set_attribute("initial_balance", initial_balance)
            
            amount = 500
            span.set_attribute("deposit_amount", amount)
            
            self.account.deposit(amount)
            
            span.set_attribute("final_balance", self.account.balance)
            span.set_attribute("expected_balance", initial_balance + amount)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            self.assertEqual(self.account.balance, initial_balance + amount)
            self.assertIn(f"{amount} deposited successfully!", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_deposit_zero(self, mock_stdout):
        with tracer.start_as_current_span("test_deposit_zero") as span:
            initial_balance = self.account.balance
            span.set_attribute("initial_balance", initial_balance)
            
            amount = 0
            span.set_attribute("deposit_amount", amount)
            
            self.account.deposit(amount)
            
            span.set_attribute("final_balance", self.account.balance)
            span.set_attribute("expected_balance", initial_balance + amount)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            self.assertEqual(self.account.balance, initial_balance + amount)
            self.assertIn(f"{amount} deposited successfully!", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_deposit_negative(self, mock_stdout):
        with tracer.start_as_current_span("test_deposit_negative") as span:
            initial_balance = self.account.balance
            span.set_attribute("initial_balance", initial_balance)
            
            amount = -100
            span.set_attribute("deposit_amount", amount)
            
            self.account.deposit(amount)
            
            span.set_attribute("final_balance", self.account.balance)
            span.set_attribute("expected_balance", initial_balance)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            # Check that balance was not changed
            self.assertEqual(self.account.balance, initial_balance)
            self.assertIn("Cannot deposit a negative amount.", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_withdraw_valid(self, mock_stdout):
        with tracer.start_as_current_span("test_withdraw_valid") as span:
            initial_balance = self.account.balance
            span.set_attribute("initial_balance", initial_balance)
            
            amount = 500
            span.set_attribute("withdraw_amount", amount)
            
            self.account.withdraw(amount)
            
            span.set_attribute("final_balance", self.account.balance)
            span.set_attribute("expected_balance", initial_balance - amount)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            self.assertEqual(self.account.balance, initial_balance - amount)
            self.assertIn(f"{amount} withdrawn successfully!", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_withdraw_zero(self, mock_stdout):
        with tracer.start_as_current_span("test_withdraw_zero") as span:
            initial_balance = self.account.balance
            span.set_attribute("initial_balance", initial_balance)
            
            amount = 0
            span.set_attribute("withdraw_amount", amount)
            
            self.account.withdraw(amount)
            
            span.set_attribute("final_balance", self.account.balance)
            span.set_attribute("expected_balance", initial_balance - amount)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            self.assertEqual(self.account.balance, initial_balance - amount)
            self.assertIn(f"{amount} withdrawn successfully!", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_withdraw_negative(self, mock_stdout):
        with tracer.start_as_current_span("test_withdraw_negative") as span:
            initial_balance = self.account.balance
            span.set_attribute("initial_balance", initial_balance)
            
            amount = -100
            span.set_attribute("withdraw_amount", amount)
            
            self.account.withdraw(amount)
            
            span.set_attribute("final_balance", self.account.balance)
            span.set_attribute("expected_balance", initial_balance)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            self.assertEqual(self.account.balance, initial_balance)
            self.assertIn("Cannot withdraw a negative amount.", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_withdraw_insufficient(self, mock_stdout):
        with tracer.start_as_current_span("test_withdraw_insufficient") as span:
            initial_balance = self.account.balance
            span.set_attribute("initial_balance", initial_balance)
            
            amount = initial_balance + 100
            span.set_attribute("withdraw_amount", amount)
            
            self.account.withdraw(amount)
            
            span.set_attribute("final_balance", self.account.balance)
            span.set_attribute("expected_balance", initial_balance)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            self.assertEqual(self.account.balance, initial_balance)
            self.assertIn("Insufficient funds.", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_balance(self, mock_stdout):
        with tracer.start_as_current_span("test_display_balance") as span:
            self.account.display_balance()
            
            span.set_attribute("owner", self.account.owner)
            span.set_attribute("balance", self.account.balance)
            span.set_attribute("output", mock_stdout.getvalue().strip())
            
            expected_output = f"Account balance for {self.account.owner} is: {self.account.balance}"
            self.assertIn(expected_output, mock_stdout.getvalue())

class TestBankAccountIntegration(unittest.TestCase):
    
    def test_transaction_sequence(self):
        with tracer.start_as_current_span("test_transaction_sequence") as span:
            account = BankAccount("Integration User", 1000)
            span.set_attribute("initial_balance", account.balance)
            
            # Define a sequence of operations
            transactions = [
                {"operation": "deposit", "amount": 500},
                {"operation": "withdraw", "amount": 200},
                {"operation": "deposit", "amount": -50},  # Should be rejected
                {"operation": "withdraw", "amount": 5000},  # Should be rejected
                {"operation": "withdraw", "amount": 100}
            ]
            
            # Execute transactions and track balance changes
            balances = [account.balance]
            
            for idx, tx in enumerate(transactions):
                with tracer.start_as_current_span(f"transaction_{idx}") as tx_span:
                    tx_span.set_attribute("operation", tx["operation"])
                    tx_span.set_attribute("amount", tx["amount"])
                    tx_span.set_attribute("balance_before", account.balance)
                    
                    if tx["operation"] == "deposit":
                        account.deposit(tx["amount"])
                    elif tx["operation"] == "withdraw":
                        account.withdraw(tx["amount"])
                    
                    tx_span.set_attribute("balance_after", account.balance)
                    balances.append(account.balance)
            
            span.set_attribute("final_balance", account.balance)
            
            # Expected balances after each transaction
            expected_balances = [1000, 1500, 1300, 1300, 1300, 1200]
            
            # Compare actual with expected
            for i, (actual, expected) in enumerate(zip(balances, expected_balances)):
                with tracer.start_as_current_span(f"balance_check_{i}") as check_span:
                    check_span.set_attribute("actual", actual)
                    check_span.set_attribute("expected", expected)
                    self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
