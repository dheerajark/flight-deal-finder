import requests
from flight_data import FlightData
from datetime import datetime, timedelta

ENDPOINT = "https://api.tequila.kiwi.com"
API_KEY = "mLIPH4WuB76OpG53SlVaGw2jnInTfXYB"

header = {
    "apikey": API_KEY
}

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def get_destination_code(self, city_name):
        parameter = {
            "term": city_name,
            "location_types": "city",
        }
        response = requests.get(url=f"{ENDPOINT}/locations/query", params=parameter, headers=header)
        data = response.json()["locations"]
        code = data[0]["code"]
        return code

    def check_flight(self, destination_city_code):
        now = datetime.now()
        to_time = datetime.now() + timedelta(days=180)
        header = {
            "apikey": API_KEY
        }
        query = {
            "fly_from": "LON",
            "fly_to": destination_city_code,
            "date_from": now.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            # "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=f"{ENDPOINT}/v2/search", params=query, headers=header)

        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(url=f"{ENDPOINT}/v2/search", params=query, headers=header)
            data = response.json()["data"][0]

            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stop_over=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        print(f"{destination_city_code}: €{flight_data.price}")
        return flight_data



