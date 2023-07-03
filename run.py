
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
import os
from termcolor import colored, cprint
import pyfiglet
from datetime import datetime
import pytz


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

# coffee_price = coffee_menu.col_values(1)

orders_spreadsheet = SHEET.worksheet('orders')
pending_orders = orders_spreadsheet.get_all_values()


# Order variables

order_list = []


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
    coffee_choice = input("\nChoose an option # (1-6): ")

    if coffee_choice == "1":
        print(f"\nThanks, you chose {coffee_menu.cell(2, 1).value}\n")
        order_list.append(coffee_menu.cell(2, 1).value)
    elif coffee_choice == "2":
        print(f"\nThanks, you chose {coffee_menu.cell(3, 1).value}\n")
        order_list.append(coffee_menu.cell(3, 1).value)
    elif coffee_choice == "3":
        print(f"\nThanks, you chose {coffee_menu.cell(4, 1).value}\n")
        order_list.append(coffee_menu.cell(4, 1).value)
    elif coffee_choice == "4":
        print(f"\nThanks, you chose {coffee_menu.cell(5, 1).value}\n")
        order_list.append(coffee_menu.cell(5, 1).value)
    elif coffee_choice == "5":
        print(f"\nThanks, you choose {coffee_menu.cell(6, 1).value}\n")
        order_list.append(coffee_menu.cell(6, 1).value)
    elif coffee_choice == "6":
        print(f"\nThanks, you chose {coffee_menu.cell(7, 1).value}\n")
        order_list.append(coffee_menu.cell(7, 1).value)

    choose_quantity()


def choose_quantity():
    """
    """
    quantity = int(input("How many of these would you like?: "))
    print(f"\nYou'd like {quantity} of these\n")
    order_list.append(quantity)

    add_more_coffees()


def add_more_coffees():
    """
    """
    more = input("Would you like to add more to the order? [y/n]: ")
    if more == "y":
        choose_coffee()
    else:
        add_customer_name()


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
    # display_pending_order()


def display_pending_order():
    """
    """
    last_order_row = len(pending_orders)
    last_order_items = orders_spreadsheet.row_values(last_order_row)

    print(f"Thanks {last_order_items[0]}, your order is:\n")
    coffees = last_order_items[1:-1:2]
    quantities = last_order_items[2::2]

    receipt = list(zip(coffees, quantities))
    print(tabulate(receipt, headers=["Coffee", "Quantity"], tablefmt="grid"))
    # calculate_total_cost(last_order_items)
    calculate_pickup_time(quantities)
    display_current_time()


def display_current_time():
    """
    """
    london_timezone = pytz.timezone('Europe/London')
    london_datetime = datetime.now(london_timezone)
    time_now = london_datetime.strftime("%H:%M")
    print(f"\nYour order was placed at {time_now}")


def calculate_total_cost(last_order_items):
    """
    """
    
    
def calculate_pickup_time(quantities):
    """
    """
    # convert 'quantities' list of strings to list of integers, using map()
    # https://www.geeksforgeeks.org/python-converting-all-strings-in-list-to-integers/
    quantities_int = list(map(int, quantities))

    sum = 0
    for num in quantities_int:
        sum = sum + num
    print(f"\nPlease give us {sum} minutes before picking up you order.")


# start screen

# print("WELCOME TO COFFEE RUN\n\n")

# print("Why wait in line!?\n")
# print("Let Coffee Run take your order,\n")
# print("and you just come collect when it's ready.\n\n")

# print("Do you wanna order some coffee?\n")
# print("[Y] - Hell yes!\n")
# print("[N] - Nah, don't know how I got here!\n")


def welcome():
    """
    """
    entrance = input("...press Y or N, then Enter: ")
    if entrance == "y":
        display_coffee_menu()

    if entrance == "n":
        print("NO")


def main():
    welcome()


main()
# display_coffee_menu()
# display_pending_order()
# print(coffee_data)
# get_current_time()