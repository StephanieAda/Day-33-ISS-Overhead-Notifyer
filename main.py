import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "hj@gmail.com"
PASSWORD = "pwword"
DUMMY_EMAIL = "kljgbfv@yahoo.com"

MY_LAT = 6.416970  # Your latitude
MY_LONG = 2.883430  # Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (MY_LAT - 5) < iss_latitude < (MY_LAT + 5) and (MY_LONG - 5) < iss_longitude < (MY_LONG + 5):
        return True


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunrise, sunset)
    time_now = datetime.now()

    if sunset < time_now.hour:
        return True


# If the ISS is close to my current position
#  And it is currently dark
#  Then email me to tell me to look up.
#  BONUS: run the code every 60 seconds.
while True:
    time.sleep(360)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.ehlo()
            connection.starttls()
            connection.ehlo()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            subject = "The International Space Station is Up Above"
            body = "Look up, its dark and The International Space Station is above Badagry right now"
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=DUMMY_EMAIL, msg=f"Subject: {subject} \n \n{body}")
