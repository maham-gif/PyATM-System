import datetime

class Account:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def check_balance(self):
        print(f"Your current balance is: ${self.balance:.2f}")

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        self.balance += amount
        self._add_transaction("Deposit", amount)
        print(f"${amount:.2f} deposited successfully.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return
        if amount > self.balance:
            print("Insufficient balance.")
            return
        self.balance -= amount
        self._add_transaction("Withdraw", amount)
        print(f"${amount:.2f} withdrawn successfully.")

    def transfer_money(self, target_account, amount):
        if amount <= 0:
            print("Invalid transfer amount.")
            return
        if amount > self.balance:
            print("Insufficient balance for transfer.")
            return
        self.balance -= amount
        target_account.balance += amount
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(
            f"{timestamp} - Transferred ${amount:.2f} to User {target_account.user_id}"
        )
        target_account.transaction_history.append(
            f"{timestamp} - Received ${amount:.2f} from User {self.user_id}"
        )
        print(f"${amount:.2f} transferred successfully to User {target_account.user_id}.")

    def change_pin(self, old_pin, new_pin):
        if self.pin != old_pin:
            print("Incorrect current PIN.")
            return False
        if old_pin == new_pin:
            print("New PIN cannot be the same as the old PIN.")
            return False
        self.pin = new_pin
        print("PIN changed successfully. Please login again with your new PIN.")
        return True

    def _add_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"{timestamp} - {transaction_type}: ${amount:.2f}")

    def show_transaction_history(self):
        print("Transaction History:")
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            for transaction in self.transaction_history:
                print(transaction)


class ATM:
    def __init__(self):
        self.accounts = {
            "1234": Account("1234", "4321", 500),
            "3456": Account("3456", "0000", 300),
            "7890": Account("7890", "1111", 700)
        }
        self.current_account = None
        self.running = True  # control main loop

    def authenticate_user(self):
        user_id = input("Enter User ID: ")
        pin = input("Enter PIN: ")
        account = self.accounts.get(user_id)
        if account and account.pin == pin:
            self.current_account = account
            print("\nLogin successful!\n")
            return True
        else:
            print("\nInvalid credentials.\n")
            return False

    def main_menu(self):
        while self.running:
            print("\n--- ATM Main Menu ---")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transaction History")
            print("5. Change PIN")
            print("6. Transfer Money")
            print("7. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.current_account.check_balance()
            elif choice == '2':
                try:
                    amount = float(input("Enter deposit amount: "))
                except ValueError:
                    print("Invalid amount entered.")
                    continue
                self.current_account.deposit(amount)
            elif choice == '3':
                try:
                    amount = float(input("Enter withdrawal amount: "))
                except ValueError:
                    print("Invalid amount entered.")
                    continue
                self.current_account.withdraw(amount)
            elif choice == '4':
                self.current_account.show_transaction_history()
            elif choice == '5':
                old_pin = input("Enter current PIN: ")
                new_pin = input("Enter new PIN: ")
                if self.current_account.change_pin(old_pin, new_pin):
                    self.current_account = None
                    print("You must login again with your new PIN.")
                    return
            elif choice == '6':
                target_id = input("Enter the User ID to transfer to (3456 or 7890 or 1234): ")
                if target_id not in self.accounts:
                    print("Target account not found.")
                elif target_id == self.current_account.user_id:
                    print("Cannot transfer to your own account.")
                else:
                    try:
                        amount = float(input("Enter amount to transfer: "))
                    except ValueError:
                        print("Invalid amount entered.")
                        continue
                    self.current_account.transfer_money(self.accounts[target_id], amount)
            elif choice == '7':
                confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
                if confirm == 'y':
                    print("Thank you for using the ATM. Goodbye!")
                    self.running = False  # end loop safely
                    return
                else:
                    print("Returning to main menu.")
            else:
                print("Invalid choice. Please try again.")

    def start(self):
        while self.running:
            if self.authenticate_user():
                self.main_menu()
            else:
                retry = input("Try again? (y/n): ").strip().lower()
                if retry != 'y':
                    print("Exiting program.")
                    break


if __name__ == "__main__":
    atm = ATM()
    atm.start()
