"""
NOLAP Pay USSD Simulator (*1145#)
Final Project - Code The Vacation With Mortoti Bootcamp
Name: [Benarkuu Gabriel Gbiel Junior]
Date: November 2025
"""

import sys
import random
import getpass

# Nolap_pay.py
# Building a Python-based command-line application for processing payments that simulates the NOLAP Pay USSD service.(*1145#)
# Global in-memory user database
user_database = {
    "0200123456": {"pin": "1234", "balance": 150.75},
    "0500654321": {"pin": "9988", "balance": 45.00},
    "0556710188": {"pin": "2000", "balance": 800.00}
}

current_user_phone = None

# Validating the functions

def validate_phone(phone):
    # Make sure the phone number is 10 digits long and contains only numbers
    return phone.isdigit() and len(phone) == 10

def validate_pin(pin):
    # Make sure the PIN is 4 digits long and contains only numbers
    return pin.isdigit() and len(pin) == 4

# Dynamic charges or fees calculation
def calculate_fee(amount):
    """0.75% fee , capped at GHS 15.00 for amounts greater than or equal to GHS 2000.00"""
    fee = amount * 0.0075
    return 15.00  if amount >= 2000 else round(fee, 2)

def calc_withdraw_fee(amount):
    """1% fee , capped at GHS 20.00 for amounts greater than or equal to GHS 2000.00"""
    fee = amount * 0.001
    return 20.00 if amount >= 2000 else round(fee, 2)

# ACCOUNT CREATION AND LOGIN
def create_account(phone):
    print("Creating a new Nolap Pay account.....")
    global user_database
    print("\n---Account Creation---")
    while True:
        pin = getpass.getpass("Set a 4-digit PIN: ")
        if not validate_pin(pin):
            print("Invalid PIN format. Please enter a 4-digit PIN.")
            continue
        confirm_pin = getpass.getpass("Confirm your PIN: ")
        if pin != confirm_pin:
            print("PINs do not match. Please try again.")
            continue
        break
    user_database[phone] = {"pin": pin, "balance": 0.0}
    print("Account created successfully!")

def login(phone):
    """For handling user login process"""
    global current_user_phone
    attempts = 3
    while attempts > 0:
        pin = getpass.getpass("Enter your 4-digit PIN: ")
        if user_database[phone]["pin"] == pin:
            current_user_phone = phone
            print("\n Login successful!")
            return True
        else:
            attempts -= 1
            print(f"Incorrect PIN. You have {attempts} attempts left.")
    print("Too many incorrect attempts. Returning to main screen.")
    return False

#  Main NOLAP Pay Menu (The *1145# Screen) that users interact with after logging in
def transfer_money():
    """This function to handle money transfer, used to send money to Nolap pay users"""
    sender = current_user_phone
    receiver = input("Enter recipient's 10-digit phone number: ")

    if not validate_phone(receiver):
        print("Invalid phone number format. Please enter a 10-digit phone number.")
        return
    if receiver not in user_database:
        print("Recipient not found on NOLAP PAY. Please check the phone number and try again.")
        return
    
    try:
        amount = float(input("Enter amount to transfer (GHS): "))
        if amount <= 0:
            print("Invalid amount. Amount must be greater than zero.")
            return
    except ValueError:
        print("Invalid input. Please enter a numeric value for the amount.")
        return  
    reference = input("Enter a reference for the transaction like (eg. fees, bills , foods): ")
    fee = calculate_fee(amount)
    total_deduction = amount + fee
    
    print(f"\nTransfer Amount: GHS {amount:.2f} to {receiver} for '{reference}'.")
    print(f"Fee: GHS {fee:.2f} | Total Deduction: GHS {total_deduction:.2f}")

    pin = getpass.getpass("Enter your PIN to confirm the transaction: ")
    if pin != user_database[sender]["pin"]:
        print("Incorrect PIN. Transaction cancelled.")
        return
    if user_database[sender]["balance"] < total_deduction:
        print("Insufficient balance. Transaction cancelled.")
        return
    # Perform the transfer
    user_database[sender]["balance"] -= total_deduction
    user_database[receiver]["balance"] += amount
    print(f"Transfer successful! GHS {amount:.2f} sent to {receiver}. Your new balance is GHS {user_database[sender]['balance']:.2f}.")

def buy_airtime():
    """Handle airtime purchase for self or for others"""
    user = current_user_phone

    print("\n--- Buy Airtime ---")
    print("1. Buy for Self")
    print("2. Buy for Another Number")
    print("0. Cancel")

    option = input("Select an option: ")

    if option == "0":
        print("Transaction cancelled.")
        return
    elif option not in ["1", "2"]:
        print("Invalid option. Please try again.")
        return

    # By determining the recipient
    if option == "1":
        recipient = user
        print(f"You selected to buy airtime for yourself ({recipient}).")
    else:
        recipient = input("Enter recipient's 10-digit phone number: ")
        if not validate_phone(recipient):
            print("Invalid phone number format. Please enter a 10-digit phone number.")
            return
        print(f"You selected to buy airtime for {recipient}.")

    try:
        amount = float(input("Enter amount of airtime to purchase (GHS): "))
        if amount <= 0:
            print("Invalid amount. Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    print(f"\nYou are about to buy GHS {amount:.2f} airtime for {recipient}.")
    confirm = input("Press 1 to Confirm or 0 to Cancel: ")
    if confirm != "1":
        print("Transaction cancelled.")
        return

    pin = getpass.getpass("Enter your PIN to confirm the transaction: ")
    if pin != user_database[user]["pin"]:
        print("Incorrect PIN. Transaction cancelled.")
        return

    if user_database[user]["balance"] < amount:
        print("Insufficient balance. Transaction cancelled.")
        return

    user_database[user]["balance"] -= amount
    txn_id = random.randint(100000, 999999)
    print(f"\nAirtime purchase successful! Transaction ID: #{txn_id}")
    print(f"GHS {amount:.2f} airtime sent to {recipient}.")
    print(f"Your new balance is GHS {user_database[user]['balance']:.2f}.")

def withdraw_deposit_menu():
    """Display and handle withdraw/deposit menu options"""
    while True:
        print("\n---Withdraw/Deposit Menu---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("0. Back to Main Menu")
        choice = input("Select an option: ")
        if choice == "1":
            deposit_money()
        elif choice == "2":
            withdraw_money()
        elif choice == "0":
            return
        else:
            print("Invalid option. Please try again.")

def withdraw_money():
    """Handle money withdrawal with fees"""
    user = current_user_phone
    try:
        amount = float(input("Enter amount to withdraw (GHS): "))
        if amount <= 0:
            print("Invalid amount. Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.") 
        return   
        
    fee = calc_withdraw_fee(amount) 
    total_deduction = amount + fee
    print(f"\nWithdraw Amount: GHS {amount:.2f}")
    print(f"Fee: GHS {fee:.2f} | Total Deduction: GHS {total_deduction:.2f}")    
    
    pin = getpass.getpass("Enter your PIN to confirm the transaction: ")
    if pin != user_database[user]["pin"]:
        print("Incorrect PIN. Transaction cancelled.")
        return
    if user_database[user]["balance"] < total_deduction:
        print("Insufficient balance. Transaction cancelled.")
        return

    user_database[user]["balance"] -= total_deduction
    token = random.randint(100000, 999999)
    print(f"Withdrawal successful! GHS {amount:.2f} withdrawn.")
    print(f"Your token is: {token}")
    print(f"Your new balance is GHS {user_database[user]['balance']:.2f}.")

def deposit_money():
    """Handle money deposits into account"""
    user = current_user_phone
    try:
        amount = float(input("Enter amount to deposit (GHS): "))
        if amount <= 0:
            print("Invalid amount. Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.") 
        return
        
    user_database[user]["balance"] += amount
    print(f"Deposit successful! GHS {amount:.2f} deposited.")
    print(f"Your new balance is GHS {user_database[user]['balance']:.2f}.")

def check_balance():
    """Check user's account balance after PIN confirmation"""
    user = current_user_phone
    pin = getpass.getpass("Enter your PIN to view balance: ")
    if pin != user_database[user]["pin"]:
        print("Incorrect PIN. Cannot display balance.")
        return
    print(f"Your current balance is GHS {user_database[user]['balance']:.2f}")

def main_menu():
    """Display and handle main menu options"""
    while True:
        print("\n=== NOLAP Pay Main Menu ===")
        print("1. Send Money")
        print("2. Buy Airtime")
        print("3. Withdraw/Deposit")
        print("4. Check Balance")
        print("5. Change PIN")
        print("0. Logout")
        
        choice = input("\nSelect an option: ")
        
        if choice == "1":
            transfer_money()
        elif choice == "2":
            buy_airtime()
        elif choice == "3":
            withdraw_deposit_menu()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            change_pin()
        elif choice == "0":
            global current_user_phone
            current_user_phone = None
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

def run_app():
    """Main application entry point"""
    print("\nWelcome to NOLAP Pay USSD Service (*1145#)")
    print("==========================================")
    
    while True:
        try:
            print("\nPlease choose an option:")
            print("1. Login")
            print("2. Create Account")
            print("0. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                phone = input("\nEnter your 10-digit phone number: ")
                if not validate_phone(phone):
                    print("Invalid phone number format. Please enter a 10-digit phone number.")
                    continue
                    
                if phone not in user_database:
                    print("Phone number not found. Please create an account first.")
                    continue
                    
                if login(phone):
                    main_menu()
                    
            elif choice == "2":
                phone = input("\nEnter your 10-digit phone number: ")
                if not validate_phone(phone):
                    print("Invalid phone number format. Please enter a 10-digit phone number.")
                    continue
                    
                if phone in user_database:
                    print("An account already exists with this phone number.")
                    continue
                    
                create_account(phone)
                
            elif choice == "0":
                print("\nThank you for using NOLAP Pay. Goodbye!")
                break
                
            else:
                print("Invalid option. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nProgram terminated by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            continue

def change_pin():
    """Change user's account PIN"""
    user = current_user_phone
    old_pin = getpass.getpass("Enter your current PIN: ")
    if old_pin != user_database[user]["pin"]:
        print("Incorrect current PIN. Cannot change PIN.")
        return
        
    while True:
        new_pin = getpass.getpass("Enter new 4-digit PIN: ")
        if not validate_pin(new_pin):
            print("Invalid PIN format. Please enter a 4-digit PIN.")
            continue
        confirm_pin = getpass.getpass("Confirm new PIN: ")
        if new_pin != confirm_pin:
            print("PINs do not match. Please try again.")
            continue
        break
        
    user_database[user]["pin"] = new_pin
    print("PIN changed successfully!")

# Update main_menu to include change_pin option
if __name__ == "__main__":
    run_app()