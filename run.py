
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
import os
from termcolor import colored, cprint
import pyfiglet


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
# pastries_menu = SHEET.worksheet('pastries_menu')

coffee_data = coffee_menu.get_all_values()
# pastries_data = pastries_menu.get_all_values()

# coffee_price = coffee_menu.col_values(1)

orders_spreadsheet = SHEET.worksheet('orders')
orders_test = orders_spreadsheet.get_all_values()

# Order variables

coffee_list = []
# customer_name = ""

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
        coffee_list.append(coffee_menu.cell(2, 1).value)
    elif coffee_choice == "2":
        print(f"\nThanks, you chose {coffee_menu.cell(3, 1).value}\n")
        coffee_list.append(coffee_menu.cell(3, 1).value)
    elif coffee_choice == "3":
        print(f"\nThanks, you chose {coffee_menu.cell(4, 1).value}\n")
        coffee_list.append(coffee_menu.cell(4, 1).value)
    elif coffee_choice == "4":
        print(f"\nThanks, you chose {coffee_menu.cell(5, 1).value}\n")
        coffee_list.append(coffee_menu.cell(5, 1).value)
    elif coffee_choice == "5":
        print(f"\nThanks, you choose {coffee_menu.cell(6, 1).value}\n")
        coffee_list.append(coffee_menu.cell(6, 1).value)
    elif coffee_choice == "6":
        print(f"\nThanks, you chose {coffee_menu.cell(7, 1).value}\n")
        coffee_list.append(coffee_menu.cell(7, 1).value)

    choose_quantity()


def choose_quantity():
    """
    """
    quantity = int(input("How many of these would you like?: "))
    print(f"\nYou'd like {quantity} of these\n")
    coffee_list.append(quantity)

    add_more_coffees()


def add_more_coffees():
    """
    """
    more = input("Would you like to add more to the order? [y/n]: ")
    if more == "y":
        choose_coffee()
    else:
        # print(tabulate(coffee_list))
        # print()
        # print(f"{coffee_list[0]} x {coffee_list[1]}")
        # print()
        # input("This is your order. Press 'Y' to send it to us: ")
        add_customer_name()


def add_customer_name():
    """
    """
    print(coffee_list)
    customer_name = input("\nWhat name should we write on your order?: ")
    if customer_name:
        send_order(coffee_list)


def send_order(order):
    """
    """
    # orders_spreadsheet = SHEET.worksheet('orders')
    orders_spreadsheet.append_row(order)


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


# main()
display_coffee_menu()
