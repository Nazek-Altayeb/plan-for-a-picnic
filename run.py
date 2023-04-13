import requests
import time
from termcolor import colored


API_KEY = "ba65189b5bb8ee63482c08473cc22602"
# BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL = "https://open-weather13.p.rapidapi.com/city"

HEADERS = {
    "X-RapidAPI-Key": "4dd693a319msh1fec678abf131f3p1954f7jsn0477517b24c6",
    "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }
Celsius = 273.15


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
            city = input('please ' + user_name + ' enter the name of the city: ')
            request_url = f"{BASE_URL}?appid={API_KEY}&q={city}"
            response = requests.get(request_url)

            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['description']
                temperature = round(data['main']['temp'] - Celsius, 2)
                print('The weather in ' + city + ' is ' + weather)
                print("and the temperature : ", temperature, "Celsius")
                break
            else:
                print(colored('An error accurred', 'red'))
        except ValueError as e:
            print(colored(f"Invalid entry: {e}\n", "red", attrs=['bold']))


def test_rapid():
    while True:
        try:
            city = input('please enter the name of the city: ')
            request_url = f"{BASE_URL}/{city}"
            response = requests.request("GET", request_url, headers=HEADERS)
            print(response.text)
            # response = requests.get(request_url)

            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['main']
                temperature = data['main']['temp']
                print('The weather in ' + city + ' is ' + weather)
                print("and the temperature : ", temperature, "Celsius")
                break
            else:
                print(colored('An error accurred', 'red'))
        except ValueError as e:
            print(colored(f"Invalid entry: {e}\n", "red", attrs=['bold']))


def main():
    test_rapid()
    # get_user_inputs()
    

main()