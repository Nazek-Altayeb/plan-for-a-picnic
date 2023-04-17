import requests
import time
from os import system, name
from termcolor import colored
import gspread
from google.oauth2.service_account import Credentials


API_KEY = "ba65189b5bb8ee63482c08473cc22602"
BASE_URL = "https://open-weather13.p.rapidapi.com/city"

HEADERS = {
    "X-RapidAPI-Key": "4dd693a319msh1fec678abf131f3p1954f7jsn0477517b24c6",
    "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
}
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('plan_for_a_picnic')


def start():
    """
    Load the project logo
    """
    clear_console()

    print("""
         _____            _____
        |  __ \\ ||     ||     ||  ||\\   ||
        | |__) | ||     ||     ||  || \\  ||
        |  ___/  ||     ||_____||  ||  \\ ||
        | |      ||     ||     ||  ||   \\||
        |_|      ||___  ||     ||  ||    \\|
        """.center(80))
    time.sleep(2)
    clear_console()
    print("starting ....")
    time.sleep(1)
    clear_console()
    options()


def clear_console():
    """
    Clear screen
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def get_user_inputs():
    """
    Get user name and the name of the city s/he is at
    """
    print("Welcome to Plan_For_A_picnic project.\n")
    time.sleep(2)
    print("We are going to ask you couple of questions .\n")
    time.sleep(2)
    print("Lets start.\n")
    time.sleep(2)
    print(colored("What is your name?", "yellow"))
    while True:
        try:
            user_name = input(colored("Enter name: ", "green")).capitalize()
            city = input('please ' + user_name +
                         ' enter the name of the city :')
            request_url = f"{BASE_URL}/{city}"
            response = requests.request("GET", request_url, headers=HEADERS)
            # print(response.text)
            # response = requests.get(request_url)

            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['main']
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                print('The weather in ' + city + ' is ' + weather + ',')
                print("the temperature : ", temperature, "Celsius, ")
                print("the humidity : ", humidity, "%.")
                break
            else:
                print(colored('An error accurred', 'red'))
        except ValueError as e:
            print(colored(f"Invalid entry: {e}\n", "red", attrs=['bold']))


def learn_about_project():
    """
    Get user name and the name of the city s/he is at
    """
    clear_console()
    print(colored("Welcome to Plan_For_A_picnic project.\n", "green"))
    print(colored("The project gives advises according to the weather condition, \nand gives recommondation for an out door picnic in next 24 hours.\n", "green"))
    back_to_main_page = input("Press enter to return back to the main page")
    if back_to_main_page is None:
        clear_console()
        options()
    else:
        clear_console()
        options()


def options():
    """
    Display available options to the user
    """
    print("1 - Learn about plan_for_a_picnic")
    print("2 - Search weather ")
    print("3 - Enter the picnic details ")
    print("Please type '1', '2' or '3' below to select the related option")
    select_option()


def select_option():
    """
    get user's selected option
    """
    try:
        option = int(input(""))
        if option == 1:
            learn_about_project()

        elif option == 2:
            main()

        elif option == 3:
            get_activity_details()

        else:
            raise ValueError
    except ValueError:
        print("Not a valid input. Please type '1' or '2' ", "your selection")
        select_option()


def get_activity_details():
    """
    get user's picnic-details (picnic duration, date time, activity, )
    """
    # sales = SHEET.worksheet('sales')
    # data = sales.get_all_values()
    # print(data)
    print("Please enter the following activity details")
    print("You will be asked to enter them one by one")
    while True:
        try:
            activity_name = input(colored("Enter the activity name: ", "green"))
            # insert into plan_for_picnic spread sheet
            if activity_name.isalpha():
                print("c")
                break
            else:
                print(colored('Only alphabetical characters allowed', 'red'))
        except ValueError as error:
            print(colored(f"Invalid entry: {error}\n", "red", attrs=['bold']))


def main():
    get_user_inputs()


start()
