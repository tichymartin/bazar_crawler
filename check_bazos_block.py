import urllib.request

from config import TEST
from send_mail import send_error_yagmail

error_message = {"subject": "BAZOŠ JE BLOKLÝ",
                 "body": "Dej vědět Martinovi"}

response = urllib.request.urlopen("http://www.bazos.cz").getcode()

if not response == 200 and not TEST:
    send_error_yagmail(error_message)

print(response)
