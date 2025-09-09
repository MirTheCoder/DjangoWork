from twilio.rest import Client
from django.conf import settings
from dotenv import load_dotenv
import os
import smtplib, ssl

load_dotenv()

def send_sms(to_number, auction, bid):
    # This creates a ssl/tls context which helps to encrypt your email
    context = ssl.create_default_context()
    # This disables any checks that are needed between the hostname and the server for the email
    # to send
    context.check_hostname = False
    # skips certificate validation
    context.verify_mode = ssl.CERT_NONE

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    print(account_sid)
    print(auth_token)
    print(from_number)
    print(to_number)

    name = bid.bidder.username
    phone = f"{to_number}@tmomail.net"

    message = f"""\
    From: {EMAIL_USERNAME}
    To: {phone}
    Subject: Auction Winner Notification

    Congrats {name}, you have won the auction for {auction.title}
    """
    try:
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
            server.sendmail(EMAIL_USERNAME, phone, message)
        print("Text Successfully sent")
    except Exception as e:
        print("Messaging Error: ", e)


    #try:
        #client = Client(account_sid, auth_token)
        #client.messages.create(
            #body=message,
            #from_=from_number,
            #to=to_number
        #)
    #except Exception as e:
        #print("Text Messaging Error: ", e)
