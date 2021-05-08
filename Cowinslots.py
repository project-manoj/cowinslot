# MIT License
#
# Copyright (c) 2021 project-manoj
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import json
import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import smtplib
import time
import sys
import os

# Global file
filename = "/tmp/slot18"

# Send an email
# if you are using gmail you need to generate app password
# as your email password wont work here
# https://support.google.com/accounts/answer/185833?hl=en for details
def send_email(msg_body):

    user_email = "user1@gmail.com"
    user_pass = "PASSWORD"
    # Uncomment for using it on Ubuntu
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # UnComment next two lines to use on CentOS
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.ehlo()

    server.login(user_email, user_pass)

    subject = "Covid Slot Check"
    msg = f"Subject: {subject}\n\n{msg_body}"
    recipients = ["user2@gmail.com"]
    # , ""]
    server.sendmail(user_email, recipients, msg)

    server.quit()


# Get District wise slot availablity
def getSlotsDistrict(district, date_now):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    url_delhi = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district}&date={date_now}"
    response = requests.get(url_delhi, headers=headers).text

    sessions = json.loads(response)["sessions"]
    for session in sessions:
        # Notify only if slots are available for age less than 45
        if (
            float(session["min_age_limit"] < 45)
            and float(session["available_capacity"]) > 1
        ):
            print("\n-------------------------------------------------------------")
            print(
                session["center_id"],
                session["name"],
                session["district_name"],
                session["pincode"],
                "\t",
                session["date"],
                " AGE LIMIT:",
                session["min_age_limit"],
                "Availability:",
                session["available_capacity"],
                session["vaccine"],
            )


# Main Program Starts from here ----->
slotFile = open(filename, "w")
original = sys.stdout
sys.stdout = slotFile
# check status of 6 days
duration = 6
date = datetime.datetime.now()
email_body = []

# district code for delhi is 9
# check for your district code
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}
url_delhi = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/9"
response = requests.get(url_delhi, headers=headers).text


for i in range(duration):
    today = f"{date.day + i}-{date.month}-{date.year}"

    districts = json.loads(response)["districts"]
    for district in districts:
        getSlotsDistrict(district["district_id"], today)

sys.stdout = original
slotFile.close()

email_body = Path(filename).read_text()
print(email_body)

# Uncomment to send email to notify
# if len(email_body) > 0:
#  send_email(email_body)
#
