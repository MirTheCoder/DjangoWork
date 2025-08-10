from django.core.mail import send_mail
from django.conf import settings
import uuid

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

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [winner_email],
            fail_silently=False
        )
        print("Message Successfully sent")
        bid.delete()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False
