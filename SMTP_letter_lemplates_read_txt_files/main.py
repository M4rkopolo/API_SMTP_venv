import smtplib
import random
import datetime as tm
import pandas
import os

EMAIL = os.environ.get('EMAIL_ONET')                #reading my email from PC enviroment
PASSWORD = os.environ.get('PASSWORD_ONET')          #pass to email also

with open("./birthdays.csv", mode="r") as days:     #open file and read as CSV
    df = pandas.read_csv(days)                          
    data = df.to_dict()                             #creating dint from df
date = tm.datetime.now()                            #saving current time

def letter_format(name):
    with open(f"./letter_templates/letter_{random.randint(1,3)}.txt") as letter:    #opening random template letter 
        text = letter.readlines()                                                   #reading letter by lines 
        letter_formatting = []
        for line in text:
            if "[NAME]" in line:                                                    #replace [NAME] to name from data dict 
                line_name = line.replace("[NAME]", name)
                letter_formatting.append(line_name)
            else:
                letter_formatting.append(line)
        return "".join(letter_formatting)
def msg(email, name):                                                               
    my_email = EMAIL
    password = PASSWORD
    with smtplib.SMTP("smtp.poczta.onet.pl") as connection:                         #preparing and sending email
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"Subject:raz dwa trzyn\n\n{letter_format(name)}"                   #calling letter_format as a content of email
        )
        print(f"We send an email to {name} to addres {email}")

for i in range(0, len(data)-1):                                                     #checking if someone have birthday today
    birth_month = data["month"][i]
    birth_day = data["day"][i]
    if birth_day == date.day and birth_month == date.month:                         #comparing current date to date from data dict
        msg(data["email"][i], data["name"][i])                                      #calling msg method with email and name inputs
