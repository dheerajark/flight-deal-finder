# from pprint import pprint
from twilio.rest import Client
from smtplib import SMTP
import dotenv
import os
# import requests

dotenv.load_dotenv()

twilio_number = os.environ.get("TWILIO_NUMBER")
my_number = os.environ.get("MY_NUMBER")

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("ACCOUNT_TOKEN")

C_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
API_KEY = os.environ.get("SHEETY_API_KEY")

header = {
    "Authorization": API_KEY
}

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def send_message(self, message1):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=twilio_number,
            to=my_number,
            body=message1
        )

        print(message.sid)

    def send_mail(self, emails, message1):

        with SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            for email in emails:
                connection.sendmail(
                    from_addr=my_email, to_addrs=email,
                    msg=f"new price alert\n\n{message1.encode('utf-8')}"
                    )

