import requests
import time
from os import system, name
from termcolor import colored


API_KEY = "ba65189b5bb8ee63482c08473cc22602"
# BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL = "https://open-weather13.p.rapidapi.com/city"

HEADERS = {
    "X-RapidAPI-Key": "4dd693a319msh1fec678abf131f3p1954f7jsn0477517b24c6",
    "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }
Celsius = 273.15


# def get_user_inputs():
#     """
#     Get user name and the name of the city s/he is at
#     """
#     print("Welcome to Plan_For_A_picnic project.\n")
#     time.sleep(2)
#     print("We are going to ask you couple of questions .\n")
#     time.sleep(2)
#     print("Lets start.\n")
#     time.sleep(2)
#     print(colored("What is your name?", "yellow"))
#     while True:
#         try:
#             user_name = input(colored("Enter name: ", "green")).capitalize()
#             city = input('please ' + user_name + ' enter the name of the city: ')
#             request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"
#             response = requests.get(request_url)

#             if response.status_code == 200:
#                 data = response.json()
#                 weather = data['weather'][0]['description']
#                 temperature = round(data['main']['temp'] - Celsius, 2)
#                 print('The weather in ' + city + ' is ' + weather)
#                 print("and the temperature : ", temperature, "Celsius")
#                 break
#             else:
#                 print(colored('An error accurred', 'red'))
#         except ValueError as e:
#             print(colored(f"Invalid entry: {e}\n", "red", attrs=['bold']))

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
            city = input('please ' + user_name + ' enter the name of the city :')
            request_url = f"{BASE_URL}/{city}"
            response = requests.request("GET", request_url, headers=HEADERS)
            print(response.text)
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


def learn_about_us():
    """
    Get user name and the name of the city s/he is at
    """
    print(colored("Welcome to Plan_For_A_picnic project.\n", "green"))
    print(colored("The project gives advises according to the weather condition, \nand gives recommondation for an out door picnic in next 24 hours.\n", "green"))
    print(colored("Please select one of the options below to proceed", "yellow"))
    options()


def options():
    """
    Display available options to the user
    """
    print("1 - Learn about plan_for_a_picnic")
    print("2 - Search weather ")
    print("Please type '1' or '2' below to select the related option")
    select_option()


def select_option():
    """
    get user's selected option
    """
    try:
        option = int(input(""))
        if option == 1:
            learn_about_us()

        elif option == 2:
            main()

        else:
            raise ValueError
    except ValueError:
        print("Not a valid input. Please type '1' or '2' ", "your selection")
        select_option()


def main():
    get_user_inputs()
    

start()