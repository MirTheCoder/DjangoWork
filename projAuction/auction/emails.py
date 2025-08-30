from django.core.mail import send_mail
from django.conf import settings
import uuid
import smtplib, ssl
import os
from dotenv import load_dotenv
load_dotenv()

#Here we are going to load our email and password from our environment variables in order to use it for sending emails
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
#You have to first generate an app password by looking up app password on google and clicking the link, and then
#following the instructions to create the app password that you will need. That password is what you will store in
#the email_password variable
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


from rest_framework.response import Response

from .models import *

#This will only be used for more secure things as a way to verify that the user is the one commiting the personal action
def generate_unique_code():
    return str(uuid.uuid4())


def notify_of_win(auction, bid):
    if not bid:
        print("Bid does not exist")
        return False

    try:
        name = bid.bidder.username
        auction_title = auction.title
        winner_email = bid.bidder.profile.email
    except Exception as e:
        print("Error getting auction/bid info:", e)
        return False

    subject = "Auction won notification"
    message = f"""
        Greetings {name},
        
        We are happy to inform you that you have been chosen as the winner of the auction titled {auction_title}.
        Please enter into your account to see the auction now within your bid log.
        
        Thank you and have a blessed rest of your day. Congratulations once again!
        """
    print(EMAIL_USERNAME)
    print(EMAIL_PASSWORD)
    print(winner_email)
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME,winner_email, message)
        print("Message Successfully sent")
        bid.delete()
        return True
    except Exception as e:
         print("Error sending email:", e)
         return False
    #try:
        #send_mail(
            #subject,
            #message,
            #settings.EMAIL_HOST_USER,
            #[winner_email],
            #fail_silently=False
        #)
        #print("Message Successfully sent")
        #bid.delete()
        #return True
    #except Exception as e:
        #print("Error sending email:", e)
        #return False
