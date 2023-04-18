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

# WEATHER_RECOMMENDATIONS = {
#         "Clouds": "Stay Inside",
#         "clear": "suitable for picnic"
#     }

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('plan_for_a_picnic')


# reference : https://github.com/Code-Institute-Submissions/pokedex/blob/main/run.py
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


# reference : https://github.com/Code-Institute-Submissions/pokedex/blob/main/run.py
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
    user_and_weather_info = None
    while True:
        try:
            user_name = input(colored("Enter name: ", "green")).capitalize()
            if not user_name.isalpha():
                raise ValueError(f"Only alphabetical characters allowed, you entered {user_name}")

            else:
                # insert name in google sheet
                break
        except ValueError as e:
            print(colored(f"Invalid entry: {e}\n", "red", attrs=['bold']))

    while True:
        try:
            city = input('please enter the name of the city :')
            if not city.isalpha():
                raise ValueError(f"Only alphabetical characters allowed, you entered {city}")

            # load weather details for the given city from the Rapid API    
            request_url = f"{BASE_URL}/{city}"
            response = requests.request("GET", request_url, headers=HEADERS)
            # print(response.text)

            if response.status_code == 200:                
                data = response.json()
                # assign weather/temperature/humidity details to local variables
                weather = data['weather'][0]['main']
                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                print('The weather in ' + city + ' is ' + weather + ',')
                print("the temperature : ", temperature, "Fahrenheit, ")
                print("the humidity : ", humidity, "%.")

                # put user and weather details in one object row
                user_and_weather_info = [user_name, city, weather, temperature, humidity]
                print('print from inner block',user_and_weather_info)

                # display recommondation to the user whether it is good idea to go out or not 
                feedback = recommondation
                recommend = feedback(temperature, humidity)
                print(recommend)

                # save user/weather/recommondation details in the google sheet
                # update_worksheet(picnic_data, "activities")

                break
            else:
                print(colored('An error accurred', 'red'))
        except ValueError as e:
            print(colored(f"Invalid entry: {e}\n", "red", attrs=['bold']))     
    print('print from outer block' ,user_and_weather_info)
    # display the options for a new round of selections
    back_to_main_page = input("Press enter to return back to the main page")
    if back_to_main_page is None:
        clear_console()
        options()
    else:
        clear_console()
        options()
    
    return user_and_weather_info


# def join_user_and_weather_info(user_name, city, weather, temperature, humidity):
#     user_and_weather_details = [user_name, city, weather, temperature, humidity]
#     return user_and_weather_details

def transfer_data_to_google_sheet():    
    user_weather_info = get_user_inputs()
    activity_info = get_activity_details()
    print('user_weather_info', user_weather_info)
    print('activity_info', activity_info)
    data = [user_weather_info, activity_info]
    update_worksheet(data, 'activities')
    # print(data)


def learn_about_project():
    """
    Get user name and the name of the city s/he is at
    """
    clear_console()
    print(colored("Welcome to Plan_For_A_picnic project.\n", "green"))
    print(colored("The project gives recommondation whether it's a good idea to go out  according to the weather condition, \n", "green"))

    # display the options for a new round of selections
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
    print("4 - Save your data in our records ")
    print("Please type '1', '2', '3' or '4' below to select the related option")
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
        
        elif option == 4:
            transfer_data_to_google_sheet()

        else:
            raise ValueError
    except ValueError:
        print("Not a valid input. Please type '1', '2', '3' or '4' ", "your selection")
        select_option()


def recommondation(temperature, humidity):
    if (temperature > 85) and (humidity > 80):
        return 'stay inside as the weather is hot and the humidity is high'
    elif (temperature < 50):
        return 'stay inside as the weather is cold'
    elif (humidity > 80):
        return 'it is unlikely you will enjoy your picnic, the humid is high out side.'
    elif (temperature >= 50) and (temperature <= 85) and (humidity <= 80):
        return 'The weather looks great, enjoy your picnic'


# reference : Code Institute (Love-Sandwiches walk through Project) 
def update_worksheet(data, worksheet):
    """
    Update worksheet, add new row with the list data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f" {worksheet} worksheet Updated successfully...\n")


def get_activity_details():
    """
    get user's picnic-details (picnic duration, date time, activity name, )
    """
    # sales = SHEET.worksheet('sales')
    # data = sales.get_all_values()
    # print(data)
    print("Please enter the following activity details")
    print("You will be asked to enter them one by one")
    activity_name = None
    while True:
        try:
            activity_name = input(colored("Enter the activity name: ", "green"))
            # insert into plan_for_picnic spread sheet
            if activity_name.isalpha():
                print('activity from inner block',activity_name)
                break
            else:
                print(colored('Only alphabetical characters allowed', 'red'))
        except ValueError as error:
            print(colored(f"Invalid entry: {error}\n", "red"))
    
    
    print('activity from outer block',activity_name)
    # display the options for a new round of selections
    back_to_main_page = input("Press enter to return back to the main page")
    if back_to_main_page is None:
        clear_console()
        options()
    else:
        clear_console()
        options()
    
    return activity_name


def main():
    get_user_inputs()


start()
