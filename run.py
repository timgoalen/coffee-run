# from CI 'love sanwiches' tutorial www.??
import gspread
from google.oauth2.service_account import Credentials

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

# print(coffee_price)


def display_coffee_menu():
    """
    Displays coffee menu from google sheets
    """
    print(coffee_price)


print("WELCOME TO COFFEE RUN\n\n")

print("Why wait in line!?\n")
print("Let Coffee Run take your order,\n")
print("and you just come collect when it's ready.\n\n")

print("Do you wanna order some coffee?\n")
print("Hell yes! (press Y then Enter)\n")
print("Nah, don't know how I got here! (press N then Enter)\n")

# make this into main()

entrance = input("Y or N: ")
if entrance == "y":
    print("YES")
    display_coffee_menu()

if entrance == "n":
    print("NO")
