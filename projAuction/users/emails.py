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
        ssl_context = ssl._create_unverified_context()
        #Here we will be populating the messsage and subjct we will add within our email
        subject = "Account Reset Code"
        messaging = f"""
        Hello {name},
        here is your special one time code, please use it in order to reset
        you password.
        
        Code: {code}
        """

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
                [email],
                connection = connection,
                fail_silently=False
            )
            print("Django Message Successfully sent")
        except Exception as e:
            print("Error sending Django email:", e)
            return False