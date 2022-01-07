import urllib.request

from send_mail import send_error_yagmail

error_message = {"subject": "BAZOŠ JE BLOKLÝ",
                 "body": "Dej vědět Martinovi"}
try:
    response = urllib.request.urlopen("http://www.bazos.cz").getcode()
except:
    send_error_yagmail(error_message)
    response = "HTTP Error 403: Forbidden"

print(response)
