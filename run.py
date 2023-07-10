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


# Import Google Sheets API,
# code from Code Institute's 'love sandwiches' tutorial.
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

# Store user data before sending to the Google Sheet database.
order_list = []
cost_list = []

# A 'switch' to choose whether or not the title text is displayed
# with staggered timings.
title_print_delay = True


# UTILITY FUNCTIONS


def clear_screen():
    """
    Clear the terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def typing_effect(text):
    """
    Create a staggered typing effect.
    """
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)


def get_user_integer_input(prompt):
    """
    Validate user input by checking it's an integer.
    """
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Sorry, that's not a digit")


# PROCEDURAL FUNCTIONS


def title():
    """
    Display the program title.
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


def introduction():
    """
    Display the introductory message.
    """
    time.sleep(1.5)
    typing_effect("Why wait in line?!")
    time.sleep(0.5)
    typing_effect("\nLet COMMAND-LINE COFFEE take your order...")
    time.sleep(2)


def enter():
    """
    Ask user if they want to see the menu.
    """

    # Clear screen and display the title again,
    # use `title_print_delay` to turn the staggered printing off.
    global title_print_delay
    title_print_delay = False
    clear_screen()
    title()

    # Display input dialogue.
    print("Shall I show you the menu?\n")
    print(colored("[Y] - Hell yes!", "light_green"))
    print(colored("[N] - Nah, don't know how I got here\n", "light_red"))
    time.sleep(1)

    # Validate user input ("y" or "n").
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
    Display the coffee menu from Google Sheets.
    """
    clear_screen()
    # Use Tabulate to format the data into a table.
    print(tabulate(COFFEE_DATA,
                   headers="firstrow", tablefmt="grid", numalign="right"))
    print()

    time.sleep(1)
    choose_coffee()


def choose_coffee():
    """
    Choose coffee type and add to `order_list` global variable.
    """
    while True:
        # Display input dialogue.
        user_input = get_user_integer_input("Choose an option # (1-6): \n")

        # Validate input between 1-6.
        if 1 <= user_input <= 6:
            # "+1" to take account of the spreadsheet title row.
            row_index = user_input + 1
            # Get coffee name from spreadsheet & update `order_list` variable.
            choice = COFFEE_MENU.cell(row_index, 1).value
            order_list.append(choice)
            # Get coffee price from spreadsheet & update `cost_list` variable.
            cost = COFFEE_MENU.cell(row_index, 2).value
            cost_list.append(cost)
            print(f"Thanks, you chose {colored(choice, 'light_green')}")
            break
        print("Whoops, the number must be between 1-6")

    choose_quantity()


def choose_quantity():
    """
    Choose coffee quantity.
    """
    while True:
        # Display input dialogue.
        message = "How many of these would you like? (1-10): \n"
        quantity = get_user_integer_input(message)
        # Validate input between 1-10.
        if 1 <= quantity <= 10:
            # Display feedback on user action.
            print(colored(f"You'd like {quantity} of these", "light_green"))
            # Update `order_list` and `coffee_list` variables.
            order_list.append(quantity)
            cost_list.append(quantity)
            break
        else:
            print('Whoops, the number must be between 1-10')

    add_more_coffees()


def add_more_coffees():
    """
    Give option to add an additional coffee type.
    """
    while True:
        # Display input dialogue.
        message = "Would you like to add more to the order? [y/n]:\n"
        customer_input = input(message).strip().lower()
        # Validate input as "y" or "n".
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
    Ask for customer name.
    """
    clear_screen()

    while True:
        # Display input dialogue.
        customer_name = input("What name should we write on your order?: \n")
        # Validate input as a string between 1-30 characters long.
        if len(customer_name) < 1 or len(customer_name) > 30:
            print("Please enter a name between 1-30 characters long")
            continue
        else:
            # Add name to start of `order_list`.
            capitalized_name = customer_name.capitalize()
            order_list.insert(0, capitalized_name)
            break

    send_order(order_list)


def send_order(order):
    """
    Update Google Sheet with all user data.
    """
    ORDERS_SPREADSHEET.append_row(order)

    display_pending_order()


def display_pending_order():
    """
    Get data on last order from Google Sheet and display in a table.
    """
    clear_screen()
    # Find the last row in the Google Sheet.
    pending_orders = ORDERS_SPREADSHEET.get_all_values()
    last_order_row = len(pending_orders)
    # Retrieve the data.
    last_order_items = ORDERS_SPREADSHEET.row_values(last_order_row)
    # Print the customer name, stored as the first cell in the row.
    print(f"Thanks {last_order_items[0]}, your order is:\n")

    # Format the retrieved row, splitting every other value into
    # `coffees` or `quantities` lists.
    coffees = last_order_items[1:-1:2]
    quantities = last_order_items[2::2]
    # Create a new list of tuples, by pairing each item in `coffees` with its
    # corresponding quantity.
    receipt = list(zip(coffees, quantities))
    # Use Tabulate to print table.
    print(tabulate(receipt, headers=["Coffee", "Quantity"], tablefmt="grid"))

    # Display cost, pickup time and order time.
    calculate_total_cost()
    calculate_pickup_time(quantities)
    display_current_time()

    time.sleep(5)
    press_enter_to_exit()


def press_enter_to_exit():
    """
    Provide option to exit the program.
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
    Calculate the number of minutes the customer should wait before collection,
    use 1 minute per 1 coffee.
    """
    # Convert `quantities` list of strings into a list of integers.
    quantities_int = list(map(int, quantities))
    # Calculate total quantity of coffee ordered.
    x = 0
    for num in quantities_int:
        x = x + num
    if x > 1:
        print(f"\nPlease give us {x} minutes before picking it up")
    elif x == 1:
        print(f"\nPlease give us {x} minute before picking it up")


def calculate_total_cost():
    """
    Calculate the total cost of the order.
    """
    # Get the prices.
    unit_price_unformatted = cost_list[::2]
    # Remove the "£" from the price, and convert into floats.
    unit_price_list = [float(price[1:]) for price in unit_price_unformatted]

    # Get the quantities.
    quantities = cost_list[1::2]
    # Convert the values in the list into integers.
    quantities = [int(quantity) for quantity in quantities]

    # Calculate the total by combining each price
    # with its corresponding quantity.
    total = 0
    for price, quantity in zip(unit_price_list, quantities):
        subtotal = price * quantity
        total += subtotal
    total_rounded = round(total, 2)

    print(f"\nThe total cost will be £{total_rounded}0")


def display_current_time():
    """
    Display the time when the order was made.
    """
    london_timezone = pytz.timezone('Europe/London')
    london_datetime = datetime.now(london_timezone)
    time_now = london_datetime.strftime("%H:%M")
    print(f"\nYour order was placed at {time_now}\n")


def goodbye_message():
    """
    Display the title and thank you message.
    """
    # Use `title_print_delay` variable to turn the staggered printing off.
    global title_print_delay
    title_print_delay = True
    clear_screen()
    print("Thanks for using\n")
    time.sleep(1)
    title()


def main():
    """
    Call the first 4 functions.
    """
    clear_screen()
    title()
    introduction()
    enter()


# Start the program.
main()
