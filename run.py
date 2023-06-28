
import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
import os

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
pastries_menu = SHEET.worksheet('pastries_menu')

coffee_data = coffee_menu.get_all_values()
pastries_data = pastries_menu.get_all_values()

coffee_price = coffee_menu.col_values(1)


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
    # print(coffee_price)
    clear_screen()
    print(tabulate(coffee_data, headers="firstrow", tablefmt="grid"))
    coffee_choice = input("\nChoose an option #: ")
    if coffee_choice == "1":
        print(f"\nThanks, you chose {coffee_menu.cell(2, 1).value}\n")
    elif coffee_choice == "2":
        print(f"\nThanks, you chose {coffee_menu.cell(3, 1).value}\n")
    elif coffee_choice == "3":
        print(f"\nThanks, you chose {coffee_menu.cell(4, 1).value}\n")
    elif coffee_choice == "4":
        print(f"\nThanks, you chose {coffee_menu.cell(5, 1).value}\n")
    elif coffee_choice == "5":
        print(f"\nThanks, you choose {coffee_menu.cell(6, 1).value}\n")
    elif coffee_choice == "6":
        print(f"\nThanks, you chose {coffee_menu.cell(7, 1).value}\n")
    choose_quantity()


def choose_quantity():
    """
    """
    quantity = input("How many of these would you like?: ")
    if quantity == "1":
        print("\nYou chose 1\n")
        display_pastries_menu()


def display_pastries_menu():
    """
    """
    print("Would you like any pastries to go with that?\n")
    print(tabulate(pastries_data, headers="firstrow", tablefmt="grid"))
    pastry_choice = input("\nChoose an option #: ")
    if pastry_choice == "1":
        print(f"\nThanks, you chose {pastries_menu.cell(2, 1).value}\n")
    elif pastry_choice == "2":
        print(f"\nThanks, you chose {pastries_menu.cell(3, 1).value}\n")
    elif pastry_choice == "3":
        print(f"\nThanks, you chose {pastries_menu.cell(4, 1).value}\n")
    choose_quantity()


print("WELCOME TO COFFEE RUN\n\n")

print("Why wait in line!?\n")
print("Let Coffee Run take your order,\n")
print("and you just come collect when it's ready.\n\n")

# print("Do you wanna order some coffee?\n")
# print("Hell yes! (press Y then Enter)\n")
# print("Nah, don't know how I got here! (press N then Enter)\n")

# question = "Do you wanna order some coffee?\n"
# options = ("[Y] - Hell yes!\n[N] - Nah, don't know how I got here!\n")
# print(question)
# print(options)

print("Do you wanna order some coffee?\n")
print("[Y] - Hell yes!\n[N] - Nah, don't know how I got here!\n")

# make this into main()

entrance = input("...press Y or N, then Enter: ")
if entrance == "y":
    print()
    display_coffee_menu()

if entrance == "n":
    print("NO")
