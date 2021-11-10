from os import listdir, getenv
from smtplib import SMTP_SSL
import ssl
import datetime
from random import choice
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
port = 465  # For SSL
email, password = getenv("EMAIL"), getenv("PASSWORD")


# Create a secure SSL context
context = ssl.create_default_context()
# 2. Check if today matches a birthday in the birthdays.csv
now = datetime.datetime.now()

dates_of_birth = pd.read_csv("birthdays.csv").to_dict(orient="records")


# 4. Send the letter generated in step 3 to that person's email address.

def send_birthday():
    for person in dates_of_birth:
        if person["month"] == now.month and person["day"] == now.day:
            letter_templates = listdir("letter_templates")
            template = choice(letter_templates)

            with open(f"letter_templates/{template}", "r") as message:
                msg = message.read().replace("[NAME]", person["name"])

            with SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(email, password)
                server.sendmail(
                    from_addr=email,
                    to_addrs=person["email"],
                    msg=f"Subject:Happy Birthday!\n\n{msg}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    send_birthday()
