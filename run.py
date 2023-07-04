import os
from datetime import datetime
import time
import pytz
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from termcolor import colored, cprint
import pyfiglet

# check deployment video for heroku imput bug

# from CI 'love sanwiches' tutorial www.??
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('coffee-run')

coffee_menu = SHEET.worksheet('coffee_menu')

coffee_data = coffee_menu.get_all_values()

orders_spreadsheet = SHEET.worksheet('orders')

# Order variables

order_list = []
cost_list = []


def clear_screen():
    """
    Clears the terminal
    """
    # https://appdividend.com/2022/06/03/how-to-clear-console-in-python/?utm_content=cmp-true
    os.system('cls' if os.name == 'nt' else 'clear')


def display_coffee_menu():
    """
    Displays coffee menu from google sheets
    """
    clear_screen()
    print(tabulate(coffee_data, headers="firstrow", tablefmt="grid", numalign="right"))
    choose_coffee()


def choose_coffee():
    """
    """
    coffee_choice = 0

    while True:
        try:
            coffee_choice = int(input("\nChoose an option # (1-6): "))
        except ValueError:
            print("Sorry, that's not a digit")
            continue
        if coffee_choice >= 1 and coffee_choice <= 6:
            if coffee_choice == 1:
                print(f"\nThanks, you chose {coffee_menu.cell(2, 1).value}\n")
                order_list.append(coffee_menu.cell(2, 1).value)
                cost_list.append(coffee_menu.cell(2, 2).value)
            elif coffee_choice == 2:
                print(f"\nThanks, you chose {coffee_menu.cell(3, 1).value}\n")
                order_list.append(coffee_menu.cell(3, 1).value)
                cost_list.append(coffee_menu.cell(3, 2).value)
            elif coffee_choice == 3:
                print(f"\nThanks, you chose {coffee_menu.cell(4, 1).value}\n")
                order_list.append(coffee_menu.cell(4, 1).value)
                cost_list.append(coffee_menu.cell(4, 2).value)
            elif coffee_choice == 4:
                print(f"\nThanks, you chose {coffee_menu.cell(5, 1).value}\n")
                order_list.append(coffee_menu.cell(5, 1).value)
                cost_list.append(coffee_menu.cell(5, 2).value)
            elif coffee_choice == 5:
                print(f"\nThanks, you choose {coffee_menu.cell(6, 1).value}\n")
                order_list.append(coffee_menu.cell(6, 1).value)
                cost_list.append(coffee_menu.cell(6, 2).value)
            elif coffee_choice == 6:
                print(f"\nThanks, you chose {coffee_menu.cell(7, 1).value}\n")
                order_list.append(coffee_menu.cell(7, 1).value)
                cost_list.append(coffee_menu.cell(7, 2).value)
            break
        else:
            print('Whoops, the number must be between 1-6')

    choose_quantity()

    
def choose_quantity():
    """
    """
    quantity = 0

    while True:
        try:
            quantity = int(input("How many of these would you like? (1-10): "))
        except ValueError:
            print("Sorry, that's not a digit")
            continue
        if quantity >= 1 and quantity <= 10:
            print(f"\nYou'd like {quantity} of these\n")
            order_list.append(quantity)
            cost_list.append(quantity)
            break
        else:
            print('Whoops, the number must be between 1-10')

    add_more_coffees()


def add_more_coffees():
    """
    """
    while True:
        customer_input = input("Would you like to add more to the order? [y/n]: ").strip().lower()
        if customer_input == "y":
            choose_coffee()
            break
        elif customer_input == "n":
            add_customer_name()
            break
        else:
            print("Sorry, this question only accepts 'y' or 'n'")
            print("(lower case or capital)")

            # old code
    # more = input("Would you like to add more to the order? [y/n]: ")
    # if more == "y":
    #     choose_coffee()
    # else:
    #     add_customer_name()


def add_customer_name():
    """
    """
    customer_name = input("\nWhat name should we write on your order?: ")
    if customer_name:
        capitalized_name = customer_name.capitalize()
        order_list.insert(0, capitalized_name)

        send_order(order_list)


def send_order(order):
    """
    """
    orders_spreadsheet.append_row(order)
    clear_screen()
    print("Sending your order to us...")
    # time.sleep(6)
    display_pending_order()


def display_pending_order():
    """
    """
    clear_screen()

    pending_orders = orders_spreadsheet.get_all_values()
    last_order_row = len(pending_orders)
    last_order_items = orders_spreadsheet.row_values(last_order_row)    
    print(f"Thanks {last_order_items[0]}, your order is:\n")

    coffees = last_order_items[1:-1:2]
    quantities = last_order_items[2::2]
    receipt = list(zip(coffees, quantities))
    print(tabulate(receipt, headers=["Coffee", "Quantity"], tablefmt="grid"))

    calculate_total_cost()
    calculate_pickup_time(quantities)
    display_current_time()
    

def calculate_pickup_time(quantities):
    """
    """
    # convert 'quantities' list of strings to list of integers, using map()
    # https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
    quantities_int = list(map(int, quantities))

    x = 0
    for num in quantities_int:
        x = x + num
    if x > 1:
        print(f"\nPlease give us {x} minutes before picking it up")
    elif x == 1:
        print(f"\nPlease give us {x} minute before picking it up")


def calculate_total_cost():
    """
    """
    unit_price_unformatted = cost_list[::2]
    # Remove the '£' from the price, and convert to float
    unit_price_list = [float(price[1:]) for price in unit_price_unformatted]

    quantities = cost_list[1::2]
    # Convert the values in the list into integers
    quantities = [int(quantity) for quantity in quantities]

    total = 0
    for price, quantity in zip(unit_price_list, quantities):
        subtotal = price * quantity
        total += subtotal
    total_rounded = round(total, 2)   
  
    print(f"\nThe total cost will be £{total_rounded}0")


def display_current_time():
    """
    """
    london_timezone = pytz.timezone('Europe/London')
    london_datetime = datetime.now(london_timezone)
    time_now = london_datetime.strftime("%H:%M")
    print(f"\nYour order was placed at {time_now}\n")


def welcome():
    """
    """
    print("WELCOME TO COMMAND-LINE COFFEE\n\n")

    time.sleep(1)
    print("Why wait in line!?\n")
    print("Let Command-Line Coffee take your order,\n")
    print("and you just come collect when it's ready.\n\n")

    time.sleep(2)
    print("Do you wanna order some coffee?\n")
    print("[Y] - Hell yes!\n")
    print("[N] - Nah, don't know how I got here!\n")


def enter():
    """
    """
    while True:
        customer_input = input("...press Y or N, then Enter: ").strip().lower()
        if customer_input == "y":
            display_coffee_menu()
            break
        elif customer_input == "n":
            print("\nSee ya next time...\n")
            break
        else:
            print("Sorry, this question only accepts 'y' or 'n'")
            print("(lower case or capital)")


def main():
    """
    """
    welcome()
    enter()


main()
# display_coffee_menu()
# display_pending_order()
# print(coffee_data)
# get_current_time()