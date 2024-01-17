import os
from dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv()

ENDPOINT = "https://api.sheety.co/dbb7ea7b850e0a064b1a6371cb8f4533/copyOfFlightDeals"
API_KEY = os.environ.get("SHEETY_API_KEY")
header = {
    "Authorization": API_KEY
}

CUSTOMERS_ENDPOINT = f"{ENDPOINT}/users"


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=f"{ENDPOINT}/prices", headers=header)
        self.data = response.json()
        self.destination_data = self.data["prices"]
        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            parameter = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{ENDPOINT}/{city['id']}", json=parameter)
            print(response.text)

    def get_customer_email(self):
        response = requests.get(url=CUSTOMERS_ENDPOINT, headers=header)
        data = response.json()
        # print(data)
        self.customer_data = data["users"]
        return self.customer_data
