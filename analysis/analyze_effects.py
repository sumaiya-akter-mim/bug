import timeit
from original_buggy_code.code import BankAccount as Code
from patched_code_versions.patch1_code import BankAccount as Patched1code
from patched_code_versions.patch2_code import BankAccount as Patched2code

def test_performance(account_class):
    def operations():
        account = account_class("Test", 1000)
        for i in range(100):
            account.deposit(10)
            account.withdraw(5)
            account.get_balance()
            account.get_transaction_history()
    return timeit.timeit(operations, number=100)

def analyze_effects():
    print("Performance Analysis:")
    print(f"Original buggy code: {test_performance(Code):.4f} seconds")
    print(f"First patch: {test_performance(Patched1code):.4f} seconds")
    print(f"Second patch: {test_performance(Patched2code):.4f} seconds")
    
    print("\nFunctionality Analysis:")
    print("- Original code has typos in transaction_history attribute")
    print("- First patch fixes the typos")
    print("- Second patch adds better encapsulation and more tracing details")
    
if __name__ == "__main__":
    analyze_effects()
