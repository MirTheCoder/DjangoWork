from django.core.mail import send_mail, get_connection
from django.conf import settings
import uuid
import smtplib
import ssl
import os
from dotenv import load_dotenv
load_dotenv()
from .models import Bids

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
    message = f"""\
    From: {EMAIL_USERNAME}
    To: {winner_email}
    Subject: Auction won notification

    Greetings {name},

    We are happy to inform you that you have been chosen as the winner of the auction titled {auction_title}.
    Please enter into your account to see the auction now within your bid log.

    Thank you and have a blessed rest of your day. Congratulations once again!
    """

    messaging = f"""\

        Greetings {name},

        This is a test for the emailing system through the django way,
        and if you are seeing this than that means that it worked
        """

    print(EMAIL_USERNAME)
    print(EMAIL_PASSWORD)
    print(winner_email)
    try:
        #This creates a ssl/tls context which helps to encrypt your email
        context = ssl.create_default_context()
        #This disables any checks that are needed between the hostname and the server for the email
        #to send
        context.check_hostname = False
        #skips certificate validation
        context.verify_mode = ssl.CERT_NONE

        #Establishes a connection with the gmail smtp server so that you can send the email through the
        #gmail system
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            #This is where we set the plain text we are sending to a more upgraded version where we send
            #a more secure email
            server.starttls(context=context)
            server.ehlo()
            #This allows us to get access to the email we want to use to send an email via gmail
            #with the required credentials
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            #This holds the content of the email we are sending along with the person we are sending to
            server.sendmail(EMAIL_USERNAME,winner_email, message)
        print("Message Successfully sent")

        #Used to bypass the ssl certificate requirement
        ssl_context = ssl._create_unverified_context()

        connection = get_connection(
            host="smtp.gmail.com",
            port=587,
            username=EMAIL_USERNAME,
            password=EMAIL_PASSWORD,
            use_tls=True,
            ssl_context=ssl_context,  # <- bypass SSL verification
        )

        try:
            send_mail(
                subject,
                messaging,
                EMAIL_USERNAME,
                [winner_email],
                connection = connection,
                fail_silently=False
            )
            print("Django Message Successfully sent")
        except Exception as e:
            print("Error sending Django email:", e)

    #Here we will grab all the bids within this auction (excluding the bid winner) to inform them
    #that a bid winner has been picked
        listOfBids = Bids.objects.filter(auction=auction).exclude(bidder__username=name)
        for bid in listOfBids:
            email = bid.bidder.profile.email
            person = bid.bidder.username
            notify = f"""\

                    Greetings {person},

                    We want to inform you that a winner for the auction {auction.title} has been selected
                    and thus all bids pertaining to this auction will be deleted. Thank you and have a
                    blessed day
                    """
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo()
                # This is where we set the plain text we are sending to a more upgraded version where we send
                # a more secure email
                server.starttls(context=context)
                server.ehlo()
                # This allows us to get access to the email we want to use to send an email via gmail
                # with the required credentials
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                # This holds the content of the email we are sending along with the person we are sending to
                server.sendmail(EMAIL_USERNAME, email, notify)

        bid.delete()
        return True
    except Exception as e:
         print("Error sending email:", e)
         return False
