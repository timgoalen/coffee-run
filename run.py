"""
"""
import os
from datetime import datetime
import time
import sys
import pytz
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from termcolor import colored
from pyfiglet import Figlet

# GLOBAL VARIABLES

# from Code Institute's 'love sandwiches' tutorial:
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open('coffee-run')
COFFEE_MENU = SHEET.worksheet('coffee_menu')
COFFEE_DATA = COFFEE_MENU.get_all_values()
ORDERS_SPREADSHEET = SHEET.worksheet('orders')

order_list = []
cost_list = []
# for the title effect to not happen after 1st time...[rephrase]
title_print_delay = True

# UTILITY FUNCTIONS


def clear_screen():
    """
    Clears the terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def typing_effect(text):
    """
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


def get_user_integer_input(prompt):
    """
    """
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Sorry, that's not a digit")
            # need 'continue' here?


# PROCEDURAL FUNCTIONS


def title():
    """
    """
    f = Figlet(font="small")
    title1 = "COMMAND"
    title2 = "LINE"
    title3 = "COFFEE."

    print(colored(f.renderText(title1), "light_cyan"))
    if title_print_delay:
        time.sleep(0.6)
    print(colored(f.renderText(title2), "light_blue"))
    if title_print_delay:
        time.sleep(0.6)
    print(colored(f.renderText(title3), "light_green"))


def welcome():
    """
    """
    time.sleep(1.5)
    typing_effect("Why wait in line?!")
    time.sleep(0.5)
    typing_effect("\nLet COMMAND-LINE COFFEE take your order...")
    time.sleep(2)


def enter():
    """
    """
    global title_print_delay
    title_print_delay = False
    clear_screen()
    title()

    print("Shall I show you the menu?\n")
    print(colored("[Y] - Hell yes!", "light_green"))
    print(colored("[N] - Nah, don't know how I got here\n", "light_red"))
    time.sleep(1)

    while True:
        customer_input = input("...press Y or N, then Enter: ").strip().lower()
        if customer_input == "y":
            break
        elif customer_input == "n":
            clear_screen()
            title()
            print("\nSee ya next time...\n")
            time.sleep(3)
            exit()
        else:
            print("Sorry, this question only accepts 'y' or 'n'")
            print("(lower case or capital)")

    display_coffee_menu()    


def display_coffee_menu():
    """
    Displays coffee menu from google sheets
    """
    clear_screen()
    print(tabulate(COFFEE_DATA, headers="firstrow", tablefmt="grid", numalign="right"))
    print()
    time.sleep(1)
    choose_coffee()


def choose_coffee():
    """
    """
    while True:
        user_input = get_user_integer_input("Choose an option # (1-6): \n")

        if 1 <= user_input <= 6:
            # user input "+ 1" to take account of the spreadsheet title row
            row_index = user_input + 1
            choice = COFFEE_MENU.cell(row_index, 1).value
            cost = COFFEE_MENU.cell(row_index, 2).value
            order_list.append(choice)
            cost_list.append(cost)
            print(f"Thanks, you chose {colored(choice, 'light_green')}")
            break
        else:
            print("Whoops, the number must be between 1-6")

    choose_quantity()


def choose_quantity():
    """
    """
    while True:
        quantity = get_user_integer_input("How many of these would you like? (1-10): \n")
        
        if 1 <= quantity <= 10:
            print(colored(f"You'd like {quantity} of these", "light_green"))
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
        customer_input = input("Would you like to add more to the order? [y/n]:\n").strip().lower()
        if customer_input == "y":
            choose_coffee()
            break
        elif customer_input == "n":
            add_customer_name()
            break
        else:
            print("Sorry, this question only accepts 'y' or 'n'")
            print("(lower case or capital)")


def add_customer_name():
    """
    """
    clear_screen()

    while True:
        customer_name = input("What name should we write on your order?: \n")

        if len(customer_name) < 1 or len(customer_name) > 30:
            print("Please enter a name between 1-30 characters long")
            continue
        else:
            capitalized_name = customer_name.capitalize()
            order_list.insert(0, capitalized_name)
            break

    send_order(order_list)


def send_order(order):
    """
    """
    ORDERS_SPREADSHEET.append_row(order)
    display_pending_order()


def display_pending_order():
    """
    """
    clear_screen()

    pending_orders = ORDERS_SPREADSHEET.get_all_values()
    last_order_row = len(pending_orders)
    last_order_items = ORDERS_SPREADSHEET.row_values(last_order_row)    
    print(f"Thanks {last_order_items[0]}, your order is:\n")

    coffees = last_order_items[1:-1:2]
    quantities = last_order_items[2::2]
    receipt = list(zip(coffees, quantities))
    print(tabulate(receipt, headers=["Coffee", "Quantity"], tablefmt="grid"))

    calculate_total_cost()
    calculate_pickup_time(quantities)
    display_current_time()

    time.sleep(5)
    press_enter_to_exit() 


def press_enter_to_exit():
    """
    """
    while True:
        user_input = input("\n\nPress Enter to EXIT:\n")
        if user_input == "":
            break
        else:
            print("Just the 'Enter' key will do. Please press to exit.")

    goodbye_message()


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


def goodbye_message():
    """
    """
    global title_print_delay
    title_print_delay = True
    clear_screen()
    print("Thanks for using\n")
    time.sleep(1)
    title()


def main():
    """
    """
    clear_screen()
    title()
    welcome()
    enter()


main()
