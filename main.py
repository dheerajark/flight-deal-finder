from data_manager import DataManager
from flight_search import FlightSearch
# from flight_data import FlightData
from notification_manager import NotificationManager

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
print(sheet_data)
flight_search = FlightSearch()
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    # print(sheet_data)
    data_manager.update_destination_code()

for destination in sheet_data:
    flight = flight_search.check_flight(destination["iataCode"])

    ###########   if the city has no flight it will continue search for another city
    if flight is None:
        continue
    ###########
    if flight.price <= destination["lowestPrice"]:
        message = (f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} "
                   f"to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to "
                   f"{flight.return_date}.")
        notification_manager = NotificationManager()
        users = data_manager.get_customer_email()
        emails = [email["email"] for email in users]
        print(emails)

        notification_manager.send_mail(emails=emails, message1=message)

        if flight.stopover > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            notification_manager.send_mail(message, emails)
