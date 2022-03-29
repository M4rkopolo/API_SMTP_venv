import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 54.516842 # my latitude
MY_LONG = 18.541941 # my longitude

PASSWORD = os.environ.get("PASSWORD")
EMAIL = os.environ.get("EMAIL")

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json") #making request to get ISS current position 
    response.raise_for_status()                                            #show status of my request
    data = response.json()                                                 #saving requested data

    iss_latitude = float(data["iss_position"]["latitude"])                  
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5  and MY_LONG-5 >= iss_longitude >= MY_LONG+5: #return TRUE if my position is within +5 or -5 degrees of the ISS position
        return True

def is_night():                                 #checking in now is night in my localization 
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)           #making request with parameters
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])                       #saveing timing of sunrise and sunset from response
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if int(time_now.hour) <= sunrise or int(time_now.hour) >= sunset:                           #comparing times to know if sun is shining now
        return True
while True:
    time.sleep(60)                                                                              #loop repeats each 60 seconds
    if is_iss_overhead() and is_night():                                                        #calling two methods if both return True then email will be sended
        my_email = EMAIL
        password = PASSWORD
        with smtplib.SMTP("smtp.poczta.onet.pl") as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="molder.iksx@gmail.com",
                msg=f"Subject: ISS is above your haed\n\nISS is above your head, look up"
            )




