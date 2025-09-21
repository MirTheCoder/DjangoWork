from django.core.mail import send_mail, get_connection
from django.conf import settings
import uuid
import smtplib
import ssl
import os
from dotenv import load_dotenv
load_dotenv()

#Here we are going to load our email and password from our environment variables in order to use it for sending emails
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
#You have to first generate an app password by looking up app password on google and clicking the link, and then
#following the instructions to create the app password that you will need. That password is what you will store in
#the email_password variable
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


def login_code(name, code, email):
        #Here we will be populating the messsage and subjct we will add within our email
        subject = "Account Reset Code"
        messaging = f"""
        Hello {name},
        here is your special one time code, please use it in order to reset
        you password.
        
        Code: {code}
        """

        try:
            # This creates a ssl/tls context which helps to encrypt your email
            context = ssl.create_default_context()
            # This disables any checks that are needed between the hostname and the server for the email
            # to send
            context.check_hostname = False
            # skips certificate validation
            context.verify_mode = ssl.CERT_NONE

            # Establishes a connection with the gmail smtp server so that you can send the email through the
            # gmail system
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
                server.sendmail(EMAIL_USERNAME, email, messaging)
            print("Message Successfully sent")
        except Exception as e:
            print("Error: ", e)