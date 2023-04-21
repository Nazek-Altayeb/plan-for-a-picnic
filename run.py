import time
from os import system, name
import requests
from termcolor import colored
import gspread
from google.oauth2.service_account import Credentials



API_KEY = "ba65189b5bb8ee63482c08473cc22602"

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('plan_for_a_picnic')

user_weather_info = ""
activity = ""


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
    global user_weather_info
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
                break
        except ValueError as error:
            print(colored(f"Invalid entry: {error}\n", "red", attrs=['bold']))

    while True:
        try:
            city = input('please enter the name of the city :')

            # load weather details for the given city from the Rapid API    
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={API_KEY}")

            if response.status_code == 200:             
                data = response.json()
                # assign weather/temperature/humidity details to local variables
                weather = data['weather'][0]['main']
                temperature = round(data['main']['temp'])
                humidity = data['main']['humidity']
                print('The weather in ' + city + ' is ' + weather + ',')
                print("the temperature : ", temperature, "Fahrenheit, ")
                print("the humidity : ", humidity, "%.")

                # put user and weather details in one object row
                user_and_weather_info = [user_name, city, weather, temperature, humidity]

                # display recommondation to the user whether it is good idea to go out or not 
                feedback = recommondation
                recommend = feedback(temperature, humidity)
                print(recommend)
                break
            else:
                print(colored('An error accurred', 'red'))
        except ValueError as error:
            print(colored(f"Invalid entry: {error}\n", "red", attrs=['bold']))     
    user_weather_info = user_and_weather_info

    # display the options for a new round of selections
    back_to_main_page = input("Press enter to return back to the main page")
    if back_to_main_page is None:
        clear_console()
        options()
    else:
        clear_console()
        options()


def transfer_data_to_google_sheet():
    """
    Transfer data to the google sheet onöy when  (user details, weather details, activity details) are exist
    """
    try:
        if (user_weather_info != "") and (activity != ""):
            user_weather_details = user_weather_info
            activity_info = activity
            data = user_weather_details + activity_info
            print('data being transfer to google sheet', data)
            update_worksheet(data, 'activities')
        else:                
            print(colored('Saving your details could be possible only when all details are exist', 'yellow'))              
    except ValueError as error:
        print(colored(f"An error accurred : {error}\n", "red", attrs=['bold'])) 

    # display the options for a new round of selections    
    back_to_main_page = input("Press enter to return back to the main page")
    if back_to_main_page is None:
        clear_console()
        options()
    else:
        clear_console()
        options()


def learn_about_project():
    """
    Get user name and the name of the city s/he is at
    """
    clear_console()
    print(colored("Welcome to Plan_For_A_picnic project.\n", "green"))
    print(colored("The project gives recommondation whether it's a good idea to go out  according to the weather condition, and all resulted data could be saved in our records once you choose to do so. \n", "green"))

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
    print("5 - Exit plan_for_a_picnic")
    print("Please type '1', '2', '3', '4' or '5' below to select the related option")
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

        elif option == 5:
            close_and_exit()

        else:
            raise ValueError
    except ValueError:
        print("Not a valid input. Please type '1', '2', '3' or '4' ", "your selection")
        select_option()


def recommondation(temperature, humidity):
    """
    Print a recommondation to the user according to the weather
    """
    if (temperature > 85) and (humidity > 80):
        return 'stay inside as the weather is hot and the humidity is high'
    elif temperature < 50:
        return 'stay inside as the weather is cold'
    elif humidity > 80:
        return 'it is unlikely you will enjoy your picnic, the humid is high out side.'
    elif (temperature >= 50) and (temperature <= 85) and (humidity <= 80):
        return 'The weather looks fine, enjoy your picnic'
    elif (temperature > 85) and (humidity < 80):
        return 'although no humid out there but it is still hot, it is you choice if you want to go out side'


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
    global activity
    print("Please enter the following activity details")
    print("You will be asked to enter them one by one")
    activity_name = None

    # enter the activity name
    while True:
        try:
            activity_name = input(colored("Enter the activity name: ", "green"))
            if activity_name.isalpha():
                break
            else:
                print(colored('Only alphabetical characters allowed', 'red'))
        except ValueError as error:
            print(colored(f"Invalid entry: {error}\n", "red"))

    # enter the activity duration
    while True:
        try:
            activity_duration = input(colored("Enter the activity duration in hours: ", "green"))
            if activity_duration.isnumeric():
                break
            else:
                print(colored('Only numeric values allowed', 'red'))
        except ValueError as error:
            print(colored(f"Invalid entry: {error}\n", "red"))

    # put activity details in one object row
    activity_info = [activity_name, activity_duration]
    activity = activity_info

    # display the options for a new round of selections   
    back_to_main_page = input("Press enter to return back to the main page")
    if back_to_main_page is None:
        clear_console()
        options()
    else:
        clear_console()
        options()


# reference : https://github.com/Code-Institute-Submissions/stock-allocation-tool
def close_and_exit():
    """
    quit plan_for_a_picnic
    """
    print("\n You are about to exit 'PLAN FOR A PICNIC'")
    time.sleep(2)
    clear_console()
    exit()   


def main():
    """
    Here the program starts
    """
    get_user_inputs()


start()